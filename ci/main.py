#!/usr/bin/env python3

import argparse
import re
from typing import List, Tuple

from dvc.repo import Repo
from dvc.repo.graph import build_graph
from dvc.stage import PipelineStage
from hera import Task, Workflow, GitArtifact, Parameter, TemplateRef


def get_unique_name(pipeline_stage: PipelineStage):
    return (
        f"{re.sub(r'[._/]', '-', pipeline_stage.dvcfile.relpath)}-{pipeline_stage.name}"
    )


def create_task(
    workflow_template: str,
    task_template: str,
    pipeline_stage: PipelineStage,
    image: str,
    git_artifact: GitArtifact,
):
    name = get_unique_name(pipeline_stage)
    target = pipeline_stage.dvcfile.relpath
    stage = pipeline_stage.name
    task = Task(
        name,
        template_ref=TemplateRef(workflow_template, task_template),
        inputs=[
            Parameter("target", target),
            Parameter("stage", stage),
            Parameter("image", image),
        ],
    )
    task.inputs.append(git_artifact)
    return task


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        help="Pipeline target. Finds all pipelines in repository if not supplied.",
        type=str,
        default=None,
    )
    parser.add_argument("--image", help="Image to run pipeline code in.", type=str)
    parser.add_argument(
        "--service_account",
        help="Optional service account to assign to pods within the workflow",
        type=str,
        default=None,
    )
    parser.add_argument("--repo", help="Git repo containing pipeline code.", type=str)
    parser.add_argument("--rev", help="Git SHA of code to execute.", type=str)
    parser.add_argument(
        "--workflow_template",
        help="Name of workflow template to use.",
        type=str,
        default="dvc-pipeline",
    )
    parser.add_argument(
        "--task_template",
        help="Name of individual task template to use.",
        type=str,
        default="dvc-stage",
    )

    args = parser.parse_args()

    repo = Repo()

    stages = repo.stage.collect(args.target)
    stage_graph = build_graph(stages)
    edges: List[Tuple[PipelineStage, PipelineStage]] = list(stage_graph.edges)

    # for each stage, maintain a collection of other stages it depends on:
    stage_to_deps = {}
    tasks = {}
    with Workflow(
        name="blah-", generate_name=True, service_account_name=args.service_account
    ) as wflow:
        git_artifact = GitArtifact("source", "/src", args.repo, args.rev)
        for (dest, src) in edges:
            dst_key = get_unique_name(dest)
            if dst_key not in stage_to_deps:
                stage_to_deps[dst_key] = []
                tasks[dst_key] = create_task(
                    args.workflow_template,
                    args.task_template,
                    dest,
                    args.image,
                    git_artifact,
                )
            if not src.is_data_source:
                src_key = get_unique_name(src)
                if src_key not in stage_to_deps:
                    stage_to_deps[src_key] = []
                    tasks[src_key] = create_task(
                        args.workflow_template,
                        args.task_template,
                        src,
                        args.image,
                        git_artifact,
                    )
                stage_to_deps[dst_key].append(src_key)

        for stage, deps in stage_to_deps.items():
            t = tasks[stage]
            for d in deps:
                t.next(tasks[d])

    wflow.create()