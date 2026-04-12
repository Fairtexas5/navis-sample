"""Deterministic curriculum task generator for Navis Web."""

from __future__ import annotations

import random
from typing import Iterable

from .site_loader import LinkDefinition, PageDefinition, TaskDefinition

CURRICULUM_TASK_IDS = [
    "curriculum_easy",
    "curriculum_medium",
    "curriculum_hard",
]


def _link(source: str, index: int, label: str, destination_page_id: str, preview_text: str) -> LinkDefinition:
    link_id = f"{source}_link_{index}"
    slug = destination_page_id.replace("_", "-")
    return LinkDefinition(
        link_id=link_id,
        label=label,
        href_slug=f"/{slug}",
        role="link",
        aria_label=f"Open {label.lower()}",
        preview_text=preview_text,
        destination_page_id=destination_page_id,
    )


def _page(page_id: str, title: str, text: str, links: Iterable[LinkDefinition]) -> PageDefinition:
    return PageDefinition(page_id=page_id, title=title, text=text, links=list(links))


def generate_curriculum_task(task_id: str, seed: int | None = None) -> TaskDefinition:
    """Generate a deterministic workflow graph with controlled ambiguity."""

    if task_id not in CURRICULUM_TASK_IDS:
        raise ValueError(f"Unknown curriculum task_id '{task_id}'")

    difficulty_index = CURRICULUM_TASK_IDS.index(task_id)
    difficulty_label = ["easy", "medium", "hard"][difficulty_index]
    rng = random.Random((seed if seed is not None else 731) + difficulty_index * 101)

    domain = ["benefits", "vendor onboarding", "claims correction"][difficulty_index]
    checkpoints = ["intake_hub", "workflow_center"]
    path_length = 4 + difficulty_index
    branch_width = 2 + difficulty_index

    pages: dict[str, PageDefinition] = {}
    intro_text = [
        "You are in a benefits portal and need the dependent verification submission form.",
        "You are in a vendor onboarding portal and need the tax validation escalation worksheet.",
        "You are in a claims correction portal and need the corrected claim exception packet.",
    ][difficulty_index]

    pages["start"] = _page(
        "start",
        f"{domain.title()} Portal Home",
        intro_text,
        [],
    )

    main_path = ["start", "intake_hub", "workflow_center"]
    while len(main_path) < path_length:
        main_path.append(f"review_stage_{len(main_path) - 2}")
    target_page_id = f"{domain.replace(' ', '_')}_target_form"
    main_path.append(target_page_id)

    for idx, page_id in enumerate(main_path):
        if page_id not in pages:
            title = (
                "Workflow Intake Hub"
                if page_id == "intake_hub"
                else "Workflow Center"
                if page_id == "workflow_center"
                else "Final Submission Form"
                if page_id == target_page_id
                else f"Review Stage {idx - 1}"
            )
            text = (
                "Choose the workflow branch that matches the requested business task."
                if page_id != target_page_id
                else "This page contains the final required submission form."
            )
            pages[page_id] = _page(page_id, title, text, [])

    distractor_labels = [
        "Billing Support",
        "General Contact",
        "Policy Updates",
        "Standard Intake",
        "Archived Requests",
        "Account Preferences",
    ]

    for idx, page_id in enumerate(main_path[:-1]):
        links: list[LinkDefinition] = []
        next_page_id = main_path[idx + 1]
        links.append(
            _link(
                page_id,
                0,
                (
                    "Dependent Verification"
                    if next_page_id == "intake_hub"
                    else "Escalated Workflow"
                    if next_page_id == "workflow_center"
                    else "Continue Review"
                    if next_page_id != target_page_id
                    else "Open Final Submission Form"
                ),
                next_page_id,
                "Continue toward the required workflow outcome.",
            )
        )

        for branch_index in range(branch_width):
            distractor_id = f"{page_id}_distractor_{branch_index}"
            if distractor_id not in pages:
                pages[distractor_id] = _page(
                    distractor_id,
                    rng.choice(distractor_labels),
                    "This area looks related but routes into a generic service path instead of the requested workflow.",
                    [],
                )
            links.append(
                _link(
                    page_id,
                    branch_index + 1,
                    rng.choice(distractor_labels),
                    distractor_id,
                    "Looks plausible, but it is not the required submission path.",
                )
            )
            if not pages[distractor_id].links:
                pages[distractor_id] = _page(
                    distractor_id,
                    pages[distractor_id].title,
                    pages[distractor_id].text,
                    [
                        _link(
                            distractor_id,
                            0,
                            "Return to workflow hub",
                            page_id,
                            "Go back and choose a different workflow branch.",
                        )
                    ],
                )

        pages[page_id] = _page(page_id, pages[page_id].title, pages[page_id].text, links)

    pages[target_page_id] = _page(
        target_page_id,
        {
            "benefits": "Dependent Verification Submission Form",
            "vendor onboarding": "Tax Validation Escalation Worksheet",
            "claims correction": "Corrected Claim Exception Packet",
        }[domain],
        "This page contains the exact final artifact requested by the workflow.",
        [],
    )

    return TaskDefinition(
        task_id=task_id,
        goal_instruction=f"Reach the final required page for the {domain} workflow without getting stuck in generic support loops.",
        start_page_id="start",
        target_page_id=target_page_id,
        max_steps=path_length + branch_width + 2,
        pages=pages,
        distractor_taxonomy=["generic support lookalikes", "archived workflow detours", "policy decoys"],
        workflow_domain=domain,
        difficulty=difficulty_label,
        required_page_ids=checkpoints,
    )
