from database import engine, SessionLocal, Base
from models import Memory
from conversation import ConversationMode
from planner import generate_project_plan
from generator import generate_project_files
from file_builder import build_project_structure
from task_engine import task_engine
from task_history import list_task_logs, read_task_log
from project_tools import open_generated_project
from system_monitor import get_system_status
from diagnostics import format_diagnostics_report
from recovery import format_recovery_result
from autonomous_patch_applier import (
    apply_autonomous_patch,
    format_patch_application,
)
from dotenv import load_dotenv
load_dotenv()
from autonomous_repair import (
    create_autonomous_repair_plan,
    format_repair_plan,
)
from autonomous_repair_applier import (
    apply_autonomous_repair,
    format_repair_application,
)
from autonomous_patcher import (
    create_patch_for_current_step,
    format_patch_plan,
)
from screen_capture import (
    capture_screen,
    format_screen_capture,
)
from screen_context import (
    describe_latest_screen,
    format_screen_context,
)
from screen_ocr import (
    read_screen_text,
    format_screen_ocr,
)
from screen_memory import (
    remember_current_screen,
    summarize_screen_memory,
    format_screen_memory_save,
    format_screen_memory_summary,
)
from screen_memory_search import (
    search_screen_memory,
    format_screen_memory_search,
)
from screen_analyzer import (
    analyze_current_screen,
    format_screen_analysis,
)
from screen_action_memory import (
    init_screen_action_memory,
    remember_screen_action_plan,
    summarize_screen_action_memory,
    format_screen_action_memory_save,
    format_screen_action_memory_summary,
)
from vision_system import (
    analyze_screen_vision,
    remember_vision_snapshot,
    load_vision_memory,
    format_vision_result,
    format_vision_memory,
)
from vision_reasoner import (
    reason_about_screen,
    format_vision_reasoning,
)
from vision_ui_mapper import (
    build_ui_map,
    format_ui_map,
)
from vision_target_finder import (
    find_visual_target,
    format_visual_target,
)
from vision_memory_search import (
    search_vision_memory,
    format_vision_memory_search,
)
from vision_workflow import (
    create_visual_workflow_plan,
    format_visual_workflow,
)
from desktop_action_safety import (
    validate_desktop_action,
    format_action_safety_result,
)
from desktop_action_queue import (
    add_desktop_action,
    get_action_queue,
    get_next_pending_action,
    mark_action_complete,
    clear_action_queue,
    format_action_queue,
    format_action_added,
)
from desktop_action_controller import (
    execute_desktop_action,
    format_desktop_action_execution,
)
from desktop_action_history import (
    remember_executed_action,
    get_action_history,
    clear_action_history,
    format_action_history,
)
from desktop_action_parser import (
    parse_desktop_action_from_text,
)
from process_manager import (
    get_service_status as get_production_service_status,
    start_ollama,
    format_service_status,
    format_start_result,
)
from startup_manager import (
    create_startup_script,
    remove_startup_script,
    check_startup_script,
    format_startup_result,
)
from app_recovery import (
    recover_jarvis_services,
    format_recovery_report,
)
from personal_memory import (
    remember_personal_item,
    get_personal_memory,
    format_personal_memory_save,
    format_personal_memory,
)
from routine_manager import (
    create_routine,
    get_routines,
    format_routine_created,
    format_routines,
)
from daily_summary import (
    generate_daily_summary,
    format_daily_summary,
)
from notification_center import (
    create_notification,
    get_notifications,
    clear_notifications,
    format_notification_created,
    format_notifications,
)
from routine_scheduler import (
    schedule_routine,
    get_routine_schedule,
    format_schedule_result,
    format_routine_schedule,
)

from voice_profile_manager import (
    update_voice_profile,
    get_voice_profile,
    format_voice_profile,
)
from personality_core import (
    apply_personality,
    format_personality_result,
)
from speech_response_builder import (
    build_spoken_response,
    format_spoken_response,
)
from speech_history import (
    remember_spoken_response,
    get_speech_history,
    format_speech_history,
)
from speech_timing import (
    estimate_speech_timing,
    format_speech_timing,
)
from voice_command_presets import (
    get_voice_preset,
    format_voice_preset,
)


from memory_core import (
    save_memory,
    list_memories,
    search_memories,
    summarize_memory,
    format_memory_saved,
    format_memory_list,
    format_memory_search,
    format_memory_summary,
)

from conversation_memory import (
    remember_exchange,
    get_recent_conversation,
    search_conversation,
    format_recent_conversation,
    format_conversation_search,
)

from memory_context_builder import (
    build_memory_context,
    format_memory_context,
)

from project_phase_memory import (
    get_project_state,
    update_project_state,
    add_project_blocker,
    format_project_state,
)

from live_ws import router as live_ws_router
from settings_api import router as settings_router

from code_editor import (
    create_file,
    read_file,
    append_file,
    delete_file,
    list_project_files,
)

from ai_file_writer import generate_file
from component_generator import generate_component_files
from component_mounter import mount_component
from launch_helper import get_launch_help
from project_analyzer import format_project_analysis
from refactor_planner import create_refactor_plan
from refactor_executor import safe_refactor_files, format_refactor_results

from safe_ai_editor import safe_improve_file
from safe_writer import safe_ai_edit
from safe_component_editor import safe_improve_component

from rollback_manager import show_backups, rollback_file

from project_memory import (
    rebuild_project_memory,
    get_project_memory,
    summarize_project_memory,
)

from autonomous_planner import (
    create_autonomous_plan,
    format_autonomous_plan,
)

from autonomous_session import (
    clear_autonomous_session,
    format_autonomous_session,
)

from autonomous_executor import (
    preview_next_autonomous_step,
    mark_next_step_complete,
    format_next_autonomous_step,
    format_step_completion,
)

from autonomous_validator import (
    run_autonomous_validation,
    format_validation_result,
)

from jarvis_logger import read_recent_logs
from log_helpers import (
    log_command,
    log_error,
    log_file_edit,
    log_component,
    log_task,
)

from command_validator import (
    validate_contains,
    validate_not_empty,
    validate_file_command_path,
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

import subprocess
import webbrowser
import os
import importlib


Base.metadata.create_all(bind=engine)

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

conversation_mode = ConversationMode()

app = FastAPI(title="JARVIS Agent API")

WORKSPACE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "workspaces",
        "coding-projects",
    )
)

print("[jarvis] backend booting...")
print(f"[jarvis] workspace: {WORKSPACE_PATH}")

try:
    init_screen_action_memory()
    print("[jarvis] screen action memory initialized.")
except Exception as e:
    print(f"[jarvis] screen action memory init failed: {e}")

app.include_router(live_ws_router)
app.include_router(settings_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Command(BaseModel):
    command: str


APP_COMMANDS = {
    "chrome": "chrome",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "vscode": "code",
    "vs code": "code",
    "calculator": "calc",
    "notepad": "notepad",
}


WEBSITE_COMMANDS = {
    "youtube": "https://youtube.com",
    "gmail": "https://gmail.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "google": "https://google.com",
}


SAFE_TERMINAL_COMMANDS = {
    "node version": "node -v",
    "python version": "py --version",
    "git version": "git --version",
    "list files": "dir",
}


BLOCKED_TASK_WORDS = [
    "format",
    "shutdown",
    "restart",
    "del /s",
    "rmdir",
    "remove-item",
    "erase",
    "reg delete",
    "taskkill /f",
    "takeown",
    "icacls",
    "diskpart",
]


def is_blocked_task(command: str):
    command_lower = command.lower()
    return any(blocked in command_lower for blocked in BLOCKED_TASK_WORDS)


def run_shell(command: str):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    output = result.stdout.strip() or result.stderr.strip()

    if not output:
        output = "Command executed."

    return output[:3000]


def normalize_path(path: str):
    path = path.strip().strip('"').strip("'")
    expanded = os.path.expanduser(path)

    if not os.path.isabs(expanded):
        expanded = os.path.join(WORKSPACE_PATH, expanded)

    return os.path.abspath(expanded)


def ask_ollama(prompt: str):
    memory_context_result = build_memory_context(prompt)

    memory_context = memory_context_result.get(
        "context",
        ""
    )

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, an advanced AI assistant "
                    "inside a Windows desktop operating system. "
                    "You help with coding, planning, automation, "
                    "business, project generation, and computer control. "
                   "Be clear, direct, cinematic, and action-focused.\n\n"
                   "You have persistent long-term memory.\n"
                   "Use the provided memory context naturally.\n"
                    "Remember project progress, goals, and workflows."
                     
                    "Remember project progress, goals, and workflows."
                ),
            },
            {
                "role": "system",
                "content": memory_context,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    answer = response.choices[0].message.content

    remember_exchange(
        prompt,
        answer,
    )

    return answer


def build_screen_action_plan():
    """
    Creates a desktop action plan from the current screen.

    This is intentionally defensive because screen_action_planner.py may
    evolve over time. It tries common planner function names first, then
    falls back to Ollama reasoning using the current screen analysis.
    """
    context_result = describe_latest_screen()
    analysis_result = analyze_current_screen()

    planner_input = {
        "screen_context": context_result,
        "screen_analysis": analysis_result,
    }

    try:
        planner_module = importlib.import_module("screen_action_planner")

        possible_function_names = [
            "generate_screen_action_plan",
            "create_screen_action_plan",
            "plan_screen_actions",
            "create_action_plan_from_screen",
        ]

        for function_name in possible_function_names:
            planner_function = getattr(planner_module, function_name, None)

            if callable(planner_function):
                try:
                    return planner_function(planner_input)
                except TypeError:
                    return planner_function()

    except Exception as e:
        print(f"[jarvis] screen action planner fallback used: {e}")

    ai_plan = ask_ollama(
        f"""
You are JARVIS with desktop awareness.

Create a clear action plan based on the user's current screen.

SCREEN CONTEXT:
{context_result}

SCREEN ANALYSIS:
{analysis_result}

Return:
1. What is happening on screen
2. What the user likely needs next
3. The next 3-7 recommended actions
4. Any risks, errors, or blockers
5. A concise final recommendation
"""
    )

    return {
        "status": "success",
        "source": "ollama_fallback",
        "plan": ai_plan,
        "screen_context": context_result,
        "screen_analysis": analysis_result,
    }


def format_screen_action_plan(result):
    if isinstance(result, str):
        return (
            "SCREEN ACTION PLAN\n\n"
            f"{result}"
        )

    if not isinstance(result, dict):
        return (
            "SCREEN ACTION PLAN\n\n"
            f"{str(result)}"
        )

    if result.get("status") == "error":
        return (
            "SCREEN ACTION PLAN ERROR\n\n"
            f"{result.get('message', 'Unknown error')}"
        )

    plan = (
        result.get("plan")
        or result.get("action_plan")
        or result.get("recommendation")
        or result.get("response")
        or result
    )

    if isinstance(plan, (dict, list)):
        import json
        plan = json.dumps(plan, indent=2)

    return (
        "SCREEN ACTION PLAN\n\n"
        f"{plan}"
    )


@app.get("/")
def root():
    return {"status": "JARVIS backend online"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "logging": "enabled",
        "rollback": "enabled",
        "validation": "enabled",
        "syntax_checker": "enabled",
        "safe_writer": "enabled",
        "safe_component_editor": "enabled",
        "project_analysis": "enabled",
        "project_memory": "enabled",
        "autonomous_planner": "enabled",
        "autonomous_sessions": "enabled",
        "autonomous_executor": "enabled",
        "autonomous_validator": "enabled",
        "autonomous_patcher": "enabled",
        "refactor_planner": "enabled",
        "refactor_executor": "enabled",
        "settings_api": "enabled",
        "diagnostics": "enabled",
        "recovery": "enabled",
        "autonomous_patch_applier": "enabled",
        "autonomous_repair": "enabled",
        "autonomous_repair_applier": "enabled",
        "screen_capture": "enabled",
        "screen_context": "enabled",
        "screen_ocr": "enabled",
        "screen_memory": "enabled",
        "screen_memory_search": "enabled",
        "screen_analyzer": "enabled",
        "screen_action_planner": "enabled",
        "screen_action_memory": "enabled",
        "vision_system": "enabled",
        "vision_memory": "enabled",
        "vision_reasoner": "enabled",
        "vision_ui_mapper": "enabled",
        "vision_target_finder": "enabled",
        "vision_memory_search": "enabled",
        "vision_workflow": "enabled",
        "desktop_action_safety": "enabled",
        "desktop_action_queue": "enabled",
        "desktop_action_controller": "enabled",
        "desktop_action_history": "enabled",
        "desktop_action_parser": "enabled",
        "process_manager": "enabled",
        "startup_manager": "enabled",
        "app_recovery": "enabled",
        "production_launcher": "enabled",
        "jarvis_tray": "available",
        "personal_memory": "enabled",
        "routine_manager": "enabled",
        "daily_summary": "enabled",
        "notification_center": "enabled",
        "routine_scheduler": "enabled",
        "voice_profile_manager": "enabled",
        "personality_core": "enabled",
        "speech_response_builder": "enabled",
        "speech_history": "enabled",
        "speech_timing": "enabled",
        "voice_command_presets": "enabled",

    }


@app.post("/project-memory/rebuild")
def project_memory_rebuild():
    try:
        result = rebuild_project_memory()
        return {
            "ok": True,
            "result": result,
        }
    except Exception as e:
        log_error(str(e))
        return {
            "ok": False,
            "error": str(e),
        }


@app.get("/project-memory")
def project_memory_get():
    try:
        memory = get_project_memory()
        return {
            "ok": True,
            "memory": memory,
        }
    except Exception as e:
        log_error(str(e))
        return {
            "ok": False,
            "error": str(e),
        }


@app.get("/project-memory/summary")
def project_memory_summary():
    try:
        summary = summarize_project_memory()
        return {
            "ok": True,
            "summary": summary,
        }
    except Exception as e:
        log_error(str(e))
        return {
            "ok": False,
            "error": str(e),
        }


@app.post("/command")
def run_command(data: Command):
    command = data.command.strip()
    lower = command.lower()

    print(f"\n[JARVIS COMMAND] {command}")

    log_command(command)

    try:
        if not command:
            return {"response": "Command cannot be empty."}

        if lower == "status":
            return {"response": "All JARVIS systems online."}

        if lower in [
            "rebuild project memory",
            "scan project memory",
            "update project memory",
        ]:
            log_task("PROJECT_MEMORY_REBUILD")

            result = rebuild_project_memory()

            systems = result.get("systems", [])
            systems_text = "\n".join(
                [f"- {system}" for system in systems]
            )

            if not systems_text:
                systems_text = "- None detected yet"

            summary = result.get("summary", {})

            return {
                "response": (
                    "Project memory rebuilt successfully.\n\n"
                    f"Total files: {summary.get('total_files', 0)}\n"
                    f"Frontend files: {summary.get('frontend_count', 0)}\n"
                    f"Backend files: {summary.get('backend_count', 0)}\n"
                    f"Other files: {summary.get('other_count', 0)}\n\n"
                    "Detected systems:\n"
                    f"{systems_text}"
                )
            }

        if lower in [
            "show project memory",
            "summarize project memory",
            "what do you know about this project",
        ]:
            log_task("PROJECT_MEMORY_SUMMARY")

            summary = summarize_project_memory()

            return {
                "response": summary
            }

        if lower.startswith("plan autonomous "):
            goal = command.replace(
                "plan autonomous ",
                "",
                1
            ).strip()

            check_goal = validate_not_empty(
                goal,
                "Autonomous goal",
            )

            if not check_goal["valid"]:
                return {
                    "response": check_goal["error"]
                }

            log_task("AUTONOMOUS_PLAN")

            result = create_autonomous_plan(goal)

            return {
                "response": format_autonomous_plan(result)
            }

        if lower == "show autonomous session":
            log_task("SHOW_AUTONOMOUS_SESSION")

            return {
                "response": format_autonomous_session()
            }

        if lower == "clear autonomous session":
            log_task("CLEAR_AUTONOMOUS_SESSION")

            clear_autonomous_session()

            return {
                "response": "Autonomous session cleared successfully."
            }

        if lower == "preview autonomous step":
            log_task("PREVIEW_AUTONOMOUS_STEP")

            result = preview_next_autonomous_step()

            return {
                "response": format_next_autonomous_step(result)
            }

        if lower == "complete autonomous step":
            log_task("COMPLETE_AUTONOMOUS_STEP")

            result = mark_next_step_complete()

            return {
                "response": format_step_completion(result)
            }

        if lower == "validate autonomous system":
            log_task("VALIDATE_AUTONOMOUS_SYSTEM")

            result = run_autonomous_validation()

            return {
                "response": format_validation_result(result)
            }

        if lower == "plan autonomous patch":
            log_task("PLAN_AUTONOMOUS_PATCH")

            result = create_patch_for_current_step()

            return {
                "response": format_patch_plan(result)
            }

        if lower == "apply autonomous patch":
            log_task("APPLY_AUTONOMOUS_PATCH")

            result = apply_autonomous_patch()

            return {
                "response": format_patch_application(result)
            }

        if lower == "plan autonomous repair":
            log_task("PLAN_AUTONOMOUS_REPAIR")

            result = create_autonomous_repair_plan()

            return {
                "response": format_repair_plan(result)
            }

        if lower == "apply autonomous repair":
            log_task("APPLY_AUTONOMOUS_REPAIR")

            result = apply_autonomous_repair()

            return {
                "response": format_repair_application(result)
            }

        if lower == "capture screen":
            log_task("CAPTURE_SCREEN")

            result = capture_screen()

            return {
                "response": format_screen_capture(result)
            }

        if lower in [
            "what is on my screen",
            "describe my screen",
            "screen context",
        ]:
            log_task("SCREEN_CONTEXT")

            result = describe_latest_screen()

            return {
                "response": format_screen_context(result)
            }

        if lower in [
            "read screen text",
            "ocr screen",
            "scan screen text",
        ]:
            log_task("SCREEN_OCR")

            result = read_screen_text()

            return {
                "response": format_screen_ocr(result)
            }

        if lower in [
            "remember screen",
            "save screen memory",
        ]:
            log_task("SCREEN_MEMORY_SAVE")

            result = remember_current_screen()

            return {
                "response": format_screen_memory_save(result)
            }

        if lower in [
            "show screen memory",
            "screen memory",
        ]:
            log_task("SCREEN_MEMORY_SUMMARY")

            result = summarize_screen_memory()

            return {
                "response": format_screen_memory_summary(result)
            }

        if lower.startswith("search screen memory for "):
            query = command.replace(
                "search screen memory for ",
                "",
                1
            ).strip()

            check_query = validate_not_empty(
                query,
                "Screen memory search query",
            )

            if not check_query["valid"]:
                return {
                    "response": check_query["error"]
                }

            log_task("SCREEN_MEMORY_SEARCH")

            result = search_screen_memory(query)

            return {
                "response": format_screen_memory_search(result)
            }

        if lower in [
            "analyze my screen",
            "analyze screen",
            "live screen analysis",
        ]:
            log_task("SCREEN_ANALYSIS")

            result = analyze_current_screen()

            return {
                "response": format_screen_analysis(result)
            }

        if lower in [
            "plan actions from screen",
            "screen action plan",
            "what should i do on screen",
        ]:
            log_task("SCREEN_ACTION_PLAN")

            result = build_screen_action_plan()

            return {
                "response": format_screen_action_plan(result)
            }

        if lower in [
            "remember screen action plan",
            "save screen action plan",
        ]:
            log_task("SCREEN_ACTION_MEMORY_SAVE")

            result = build_screen_action_plan()
            saved = remember_screen_action_plan(result)

            return {
                "response": format_screen_action_memory_save(saved)
            }

        if lower in [
            "show screen action memory",
            "screen action memory",
        ]:
            log_task("SCREEN_ACTION_MEMORY_SUMMARY")

            result = summarize_screen_action_memory()

            return {
                "response": format_screen_action_memory_summary(result)
            }


        if lower in [
            "real vision",
            "analyze screen vision",
            "vision system",
            "phase 9 vision",
        ]:
            log_task("PHASE_9_REAL_VISION")

            result = analyze_screen_vision()

            return {
                "response": format_vision_result(result)
            }

        if lower in [
            "remember vision",
            "save vision snapshot",
            "remember screen vision",
        ]:
            log_task("PHASE_9_VISION_MEMORY_SAVE")

            result = analyze_screen_vision()
            saved = remember_vision_snapshot(result)

            return {
                "response": (
                    format_vision_result(result)
                    + "\n\n"
                    + saved.get("message", "Vision snapshot saved.")
                )
            }

        if lower in [
            "show vision memory",
            "vision memory",
            "show screen vision memory",
        ]:
            log_task("PHASE_9_VISION_MEMORY_SUMMARY")

            result = load_vision_memory()

            return {
                "response": format_vision_memory(result)
            }


        if lower in [
            "explain my screen",
            "vision reason",
            "what am i looking at",
        ]:
            log_task("PHASE_9_VISION_REASONING")

            result = reason_about_screen()

            return {
                "response": format_vision_reasoning(result)
            }

        if lower in [
            "map screen ui",
            "ui map",
            "map my screen",
            "visual ui map",
        ]:
            log_task("PHASE_9_UI_MAP")

            result = build_ui_map()

            return {
                "response": format_ui_map(result)
            }

        if lower.startswith("find visual target "):
            query = command.replace(
                "find visual target ",
                "",
                1
            ).strip()

            check_query = validate_not_empty(
                query,
                "Visual target query",
            )

            if not check_query["valid"]:
                return {
                    "response": check_query["error"]
                }

            log_task("PHASE_9_VISUAL_TARGET_FINDER")

            result = find_visual_target(query)

            return {
                "response": format_visual_target(result)
            }

        if lower.startswith("search vision memory for "):
            query = command.replace(
                "search vision memory for ",
                "",
                1
            ).strip()

            check_query = validate_not_empty(
                query,
                "Vision memory search query",
            )

            if not check_query["valid"]:
                return {
                    "response": check_query["error"]
                }

            log_task("PHASE_9_VISION_MEMORY_SEARCH")

            result = search_vision_memory(query)

            return {
                "response": format_vision_memory_search(result)
            }

        if lower.startswith("visual workflow "):
            goal = command.replace(
                "visual workflow ",
                "",
                1
            ).strip()

            check_goal = validate_not_empty(
                goal,
                "Visual workflow goal",
            )

            if not check_goal["valid"]:
                return {
                    "response": check_goal["error"]
                }

            log_task("PHASE_9_VISUAL_WORKFLOW")

            result = create_visual_workflow_plan(goal)

            return {
                "response": format_visual_workflow(result)
            }


        if lower.startswith("test desktop action "):
            try:
                action = parse_desktop_action_from_text(command)
            except Exception as e:
                return {
                    "response": (
                        "DESKTOP ACTION PARSE ERROR\n\n"
                        f"{str(e)}"
                    )
                }

            log_task("DESKTOP_ACTION_SAFETY_TEST")

            result = validate_desktop_action(action)

            return {
                "response": format_action_safety_result(result)
            }

        if lower.startswith("queue desktop action ") or lower.startswith("queue click ") or lower.startswith("queue double click ") or lower.startswith("queue right click ") or lower.startswith("queue move mouse ") or lower.startswith("queue type ") or lower.startswith("queue press ") or lower.startswith("queue hotkey ") or lower.startswith("queue scroll ") or lower.startswith("queue wait "):
            queue_command = command

            if lower.startswith("queue ") and not lower.startswith("queue desktop action "):
                queue_command = "queue desktop action " + command.replace("queue ", "", 1)

            try:
                action = parse_desktop_action_from_text(queue_command)
            except Exception as e:
                return {
                    "response": (
                        "DESKTOP ACTION PARSE ERROR\n\n"
                        f"{str(e)}"
                    )
                }

            log_task("DESKTOP_ACTION_QUEUE_ADD")

            result = add_desktop_action(action)

            return {
                "response": format_action_added(result)
            }

        if lower in [
            "show desktop action queue",
            "desktop action queue",
            "show action queue",
        ]:
            log_task("DESKTOP_ACTION_QUEUE_SHOW")

            result = get_action_queue()

            return {
                "response": format_action_queue(result)
            }

        if lower in [
            "clear desktop action queue",
            "clear action queue",
        ]:
            log_task("DESKTOP_ACTION_QUEUE_CLEAR")

            result = clear_action_queue()

            return {
                "response": result.get("message", "Desktop action queue cleared.")
            }

        if lower in [
            "confirm desktop action",
            "execute desktop action",
            "run desktop action",
        ]:
            log_task("DESKTOP_ACTION_EXECUTE_CONFIRMED")

            pending = get_next_pending_action()

            if not pending.get("success"):
                return {
                    "response": pending.get("error")
                }

            queued_action = pending.get("queued_action")
            action = queued_action.get("action")

            execution = execute_desktop_action(action)

            mark_action_complete(
                queued_action.get("id"),
                success=execution.get("success"),
                message=execution.get("message") or execution.get("error"),
            )

            remember_executed_action(
                action,
                success=execution.get("success"),
                result_message=execution.get("message") or execution.get("error"),
            )

            return {
                "response": format_desktop_action_execution(execution)
            }

        if lower in [
            "show desktop action history",
            "desktop action history",
            "show action history",
        ]:
            log_task("DESKTOP_ACTION_HISTORY_SHOW")

            result = get_action_history()

            return {
                "response": format_action_history(result)
            }

        if lower in [
            "clear desktop action history",
            "clear action history",
        ]:
            log_task("DESKTOP_ACTION_HISTORY_CLEAR")

            result = clear_action_history()

            return {
                "response": result.get("message", "Desktop action history cleared.")
            }


        if lower in [
            "production status",
            "jarvis production status",
            "service status",
        ]:
            log_task("PHASE_11_PRODUCTION_STATUS")

            status = get_production_service_status()

            return {
                "response": format_service_status(status)
            }

        if lower in [
            "recover jarvis",
            "production recovery",
            "repair production services",
            "restart jarvis services",
        ]:
            log_task("PHASE_11_PRODUCTION_RECOVERY")

            result = recover_jarvis_services()

            return {
                "response": format_recovery_report(result)
            }

        if lower in [
            "start ollama service",
            "start ollama production",
        ]:
            log_task("PHASE_11_START_OLLAMA")

            result = start_ollama()

            return {
                "response": format_start_result(result)
            }

        if lower in [
            "enable jarvis startup",
            "enable startup",
            "start jarvis with windows",
        ]:
            log_task("PHASE_11_ENABLE_STARTUP")

            result = create_startup_script()

            return {
                "response": format_startup_result(result)
            }

        if lower in [
            "disable jarvis startup",
            "disable startup",
            "stop jarvis from starting with windows",
        ]:
            log_task("PHASE_11_DISABLE_STARTUP")

            result = remove_startup_script()

            return {
                "response": format_startup_result(result)
            }

        if lower in [
            "check jarvis startup",
            "startup status",
            "check startup",
        ]:
            log_task("PHASE_11_CHECK_STARTUP")

            result = check_startup_script()

            return {
                "response": format_startup_result(result)
            }


        if lower.startswith("remember personal preference "):
            content_text = command.replace(
                "remember personal preference ",
                "",
                1
            ).strip()

            check_content = validate_not_empty(
                content_text,
                "Personal preference",
            )

            if not check_content["valid"]:
                return {
                    "response": check_content["error"]
                }

            log_task("PHASE_12_PERSONAL_MEMORY_SAVE")

            result = remember_personal_item(
                "preference",
                content_text,
            )

            return {
                "response": format_personal_memory_save(result)
            }

        if lower.startswith("remember personal goal "):
            content_text = command.replace(
                "remember personal goal ",
                "",
                1
            ).strip()

            check_content = validate_not_empty(
                content_text,
                "Personal goal",
            )

            if not check_content["valid"]:
                return {
                    "response": check_content["error"]
                }

            log_task("PHASE_12_PERSONAL_GOAL_SAVE")

            result = remember_personal_item(
                "goal",
                content_text,
            )

            return {
                "response": format_personal_memory_save(result)
            }

        if lower.startswith("remember work habit "):
            content_text = command.replace(
                "remember work habit ",
                "",
                1
            ).strip()

            check_content = validate_not_empty(
                content_text,
                "Work habit",
            )

            if not check_content["valid"]:
                return {
                    "response": check_content["error"]
                }

            log_task("PHASE_12_WORK_HABIT_SAVE")

            result = remember_personal_item(
                "work_habit",
                content_text,
            )

            return {
                "response": format_personal_memory_save(result)
            }

        if lower in [
            "show personal memory",
            "personal memory",
            "show ai os memory",
        ]:
            log_task("PHASE_12_PERSONAL_MEMORY_SHOW")

            result = get_personal_memory()

            return {
                "response": format_personal_memory(result)
            }

        if lower.startswith("create routine "):
            body = command.replace(
                "create routine ",
                "",
                1
            ).strip()

            check_body = validate_contains(
                body,
                " steps ",
                "create routine ROUTINE_NAME steps STEP 1; STEP 2; STEP 3",
            )

            if not check_body["valid"]:
                return {
                    "response": check_body["error"]
                }

            split_index = body.lower().index(" steps ")
            name = body[:split_index].strip()
            steps_text = body[split_index + len(" steps "):].strip()

            check_name = validate_not_empty(name, "Routine name")
            if not check_name["valid"]:
                return {"response": check_name["error"]}

            check_steps = validate_not_empty(steps_text, "Routine steps")
            if not check_steps["valid"]:
                return {"response": check_steps["error"]}

            steps = [
                step.strip()
                for step in steps_text.split(";")
                if step.strip()
            ]

            log_task("PHASE_12_ROUTINE_CREATE")

            result = create_routine(name, steps)

            return {
                "response": format_routine_created(result)
            }

        if lower in [
            "show routines",
            "show jarvis routines",
            "routines",
        ]:
            log_task("PHASE_12_ROUTINES_SHOW")

            result = get_routines()

            return {
                "response": format_routines(result)
            }

        if lower.startswith("schedule routine "):
            body = command.replace(
                "schedule routine ",
                "",
                1
            ).strip()

            check_body = validate_contains(
                body,
                " at ",
                "schedule routine ROUTINE_NAME at TIME",
            )

            if not check_body["valid"]:
                return {
                    "response": check_body["error"]
                }

            split_index = body.lower().index(" at ")
            name = body[:split_index].strip()
            time_of_day = body[split_index + len(" at "):].strip()

            log_task("PHASE_12_ROUTINE_SCHEDULE")

            result = schedule_routine(name, time_of_day)

            return {
                "response": format_schedule_result(result)
            }

        if lower in [
            "show routine schedule",
            "routine schedule",
            "show scheduled routines",
        ]:
            log_task("PHASE_12_ROUTINE_SCHEDULE_SHOW")

            result = get_routine_schedule()

            return {
                "response": format_routine_schedule(result)
            }

        if lower in [
            "run daily summary",
            "daily summary",
            "show daily summary",
        ]:
            log_task("PHASE_12_DAILY_SUMMARY")

            result = generate_daily_summary()

            return {
                "response": format_daily_summary(result)
            }

        if lower.startswith("create notification "):
            message = command.replace(
                "create notification ",
                "",
                1
            ).strip()

            check_message = validate_not_empty(
                message,
                "Notification message",
            )

            if not check_message["valid"]:
                return {
                    "response": check_message["error"]
                }

            log_task("PHASE_12_NOTIFICATION_CREATE")

            result = create_notification(message)

            return {
                "response": format_notification_created(result)
            }

        if lower in [
            "show notifications",
            "notifications",
            "notification center",
        ]:
            log_task("PHASE_12_NOTIFICATIONS_SHOW")

            result = get_notifications()

            return {
                "response": format_notifications(result)
            }

        if lower in [
            "clear notifications",
            "clear notification center",
        ]:
            log_task("PHASE_12_NOTIFICATIONS_CLEAR")

            result = clear_notifications()

            return {
                "response": result.get("message", "Notifications cleared.")
            }


        if lower in [
            "show jarvis voice profile",
            "voice profile",
            "show voice profile",
        ]:
            log_task("PHASE_13A_VOICE_PROFILE")

            result = get_voice_profile()

            return {
                "response": format_voice_profile(result)
            }

        if lower.startswith("set jarvis tone "):
            tone = command.replace(
                "set jarvis tone ",
                "",
                1
            ).strip().lower()

            valid_tones = [
                "cinematic",
                "technical",
                "calm",
                "urgent",
            ]

            if tone not in valid_tones:
                return {
                    "response": (
                        "Invalid tone.\n\n"
                        f"Available tones: {', '.join(valid_tones)}"
                    )
                }

            log_task("PHASE_13A_SET_TONE")

            result = update_voice_profile(
                "tone",
                tone,
            )

            return {
                "response": format_voice_profile(result)
            }

        if lower.startswith("apply jarvis personality "):
            text = command.replace(
                "apply jarvis personality ",
                "",
                1
            ).strip()

            check_text = validate_not_empty(
                text,
                "Personality text",
            )

            if not check_text["valid"]:
                return {
                    "response": check_text["error"]
                }

            log_task("PHASE_13A_PERSONALITY")

            result = apply_personality(text)

            remember_spoken_response(
                result.get("response"),
                tone=result.get("tone"),
                category="personality",
            )

            return {
                "response": format_personality_result(result)
            }

        if lower.startswith("build spoken response "):
            text = command.replace(
                "build spoken response ",
                "",
                1
            ).strip()

            check_text = validate_not_empty(
                text,
                "Spoken response text",
            )

            if not check_text["valid"]:
                return {
                    "response": check_text["error"]
                }

            log_task("PHASE_13A_SPOKEN_RESPONSE")

            result = build_spoken_response(text)

            remember_spoken_response(
                result.get("spoken_response"),
                category="spoken_response",
            )

            return {
                "response": format_spoken_response(result)
            }

        if lower.startswith("estimate speech timing "):
            text = command.replace(
                "estimate speech timing ",
                "",
                1
            ).strip()

            check_text = validate_not_empty(
                text,
                "Speech timing text",
            )

            if not check_text["valid"]:
                return {
                    "response": check_text["error"]
                }

            log_task("PHASE_13A_SPEECH_TIMING")

            result = estimate_speech_timing(text)

            return {
                "response": format_speech_timing(result)
            }

        if lower in [
            "show speech history",
            "speech history",
        ]:
            log_task("PHASE_13A_SPEECH_HISTORY")

            result = get_speech_history()

            return {
                "response": format_speech_history(result)
            }

        if lower in [
            "speak status",
            "speak diagnostics",
            "speak daily summary",
            "speak workflow",
            "speak screen analysis",
        ]:
            log_task("PHASE_13A_VOICE_PRESET")

            result = get_voice_preset(lower)

            if result.get("success"):
                remember_spoken_response(
                    result.get("response"),
                    category="voice_preset",
                )

            return {
                "response": format_voice_preset(result)
            }


        if lower in [
            "diagnose yourself",
            "self diagnostics",
            "run diagnostics",
        ]:
            log_task("SELF_DIAGNOSTICS")

            return {
                "response": format_diagnostics_report()
            }

        if lower in [
            "restart ollama",
            "repair ollama",
            "repair voice",
            "check voice",
            "scan logs",
            "scan logs for errors",
            "restart frontend",
            "relaunch frontend",
        ]:
            log_task("RECOVERY_ACTION")

            return {
                "response": format_recovery_result(lower)
            }

        if lower == "launch help":
            return {"response": get_launch_help()}

        if lower == "show logs":
            return {"response": read_recent_logs()}

        if lower == "show backups":
            return {"response": show_backups()}

        if lower == "analyze project":
            log_task("PROJECT_ANALYSIS")
            return {"response": format_project_analysis()}

        if lower.startswith("plan refactor "):
            instruction = command.replace("plan refactor ", "", 1).strip()

            check_instruction = validate_not_empty(
                instruction,
                "Refactor instruction",
            )

            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            log_task("REFACTOR_PLAN")

            plan = create_refactor_plan(instruction)

            return {
                "response": (
                    "JARVIS REFACTOR PLAN\n\n"
                    f"{plan}"
                )
            }

        if lower.startswith("safe refactor files "):
            body = command.replace("safe refactor files ", "", 1).strip()

            check = validate_contains(
                body,
                " by ",
                "safe refactor files FILE1, FILE2 by INSTRUCTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" by ")
            files_part = body[:split_index].strip()
            instruction = body[split_index + len(" by "):].strip()

            check_files = validate_not_empty(files_part, "Files")
            if not check_files["valid"]:
                return {"response": check_files["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            relative_paths = [
                item.strip()
                for item in files_part.split(",")
                if item.strip()
            ]

            if not relative_paths:
                return {"response": "No valid files were provided."}

            result = safe_refactor_files(relative_paths, instruction)

            log_task("SAFE_MULTI_FILE_REFACTOR")

            for item in result["results"]:
                if item.get("success") and item.get("path"):
                    log_file_edit(item["path"])
                elif item.get("error"):
                    log_error(item["error"])

            return {"response": format_refactor_results(result)}

        if lower == "system status":
            status = get_system_status()

            return {
                "response": (
                    "SYSTEM STATUS\n\n"
                    f"Node: {status['node']}\n"
                    f"System: {status['system']}\n"
                    f"CPU: {status['cpu_percent']}%\n"
                    f"Memory: {status['memory_percent']}%\n"
                    f"Disk: {status['disk_percent']}%"
                )
            }

        if lower.startswith("rollback file "):
            body = command.replace("rollback file ", "", 1).strip()

            check = validate_contains(
                body,
                " to ",
                "rollback file BACKUP_NAME to TARGET_PATH",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" to ")
            backup_name = body[:split_index].strip()
            raw_target_path = body[split_index + len(" to "):].strip()

            check_backup = validate_not_empty(backup_name, "Backup name")
            if not check_backup["valid"]:
                return {"response": check_backup["error"]}

            check_path = validate_file_command_path(raw_target_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            target_path = normalize_path(raw_target_path)

            result = rollback_file(backup_name, target_path)

            if not result["success"]:
                log_error(result["error"])
                return {"response": f"Rollback Error:\n{result['error']}"}

            log_file_edit(target_path)

            return {"response": result["message"]}

        if lower.startswith("safe improve component "):
            body = command.replace("safe improve component ", "", 1).strip()

            check = validate_contains(
                body,
                " by ",
                "safe improve component COMPONENT_NAME by INSTRUCTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" by ")
            component_name = body[:split_index].strip().replace(" ", "")
            instruction = body[split_index + len(" by "):].strip()

            check_component = validate_not_empty(component_name, "Component name")
            if not check_component["valid"]:
                return {"response": check_component["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            result = safe_improve_component(component_name, instruction)

            if not result["success"]:
                log_error(result["error"])

                rollback_text = ""
                if result.get("rolled_back"):
                    rollback_text = "\n\nRollback: completed automatically."

                return {
                    "response": (
                        "Safe Component Improve Error:\n"
                        f"{result['error']}"
                        f"{rollback_text}"
                    )
                }

            log_component(component_name)

            return {
                "response": (
                    "Safe component improvement completed.\n\n"
                    f"Component: {result['component']}\n"
                    f"TSX: {result['tsx_path']}\n"
                    f"CSS: {result['css_path']}\n"
                    f"TSX Backup: {result['tsx_backup']}\n"
                    f"CSS Backup: {result['css_backup']}\n"
                    f"Syntax: {result['syntax'] or 'Passed'}"
                )
            }

        if lower.startswith("safe edit file "):
            body = command.replace("safe edit file ", "", 1).strip()

            check = validate_contains(
                body,
                " by ",
                "safe edit file PATH by INSTRUCTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" by ")
            raw_path = body[:split_index].strip()
            instruction = body[split_index + len(" by "):].strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            path = normalize_path(raw_path)
            result = safe_ai_edit(path, instruction)

            if not result["success"]:
                log_error(result["error"])

                backup_text = ""
                if "backup" in result:
                    backup_text = f"\n\nBackup created:\n{result['backup']}"

                rollback_text = ""
                if result.get("rolled_back"):
                    rollback_text = "\nRollback: completed automatically."

                return {
                    "response": (
                        "Safe Edit Error:\n"
                        f"{result['error']}"
                        f"{backup_text}"
                        f"{rollback_text}"
                    )
                }

            log_file_edit(path)

            return {
                "response": (
                    "Safe AI edit completed.\n\n"
                    f"File: {result['path']}\n"
                    f"Backup: {result['backup']}\n"
                    f"Syntax: {result['syntax'] or 'Passed'}"
                )
            }

        if lower.startswith("safe improve file "):
            body = command.replace("safe improve file ", "", 1).strip()

            check = validate_contains(
                body,
                " by ",
                "safe improve file PATH by INSTRUCTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" by ")
            raw_path = body[:split_index].strip()
            instruction = body[split_index + len(" by "):].strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            path = normalize_path(raw_path)
            result = safe_improve_file(path, instruction)

            if not result["success"]:
                log_error(result["error"])

                backup_text = ""
                if "backup" in result:
                    backup_text = f"\n\nBackup created:\n{result['backup']}"

                return {
                    "response": (
                        "Safe Improve Error:\n"
                        f"{result['error']}"
                        f"{backup_text}"
                    )
                }

            log_file_edit(path)

            return {
                "response": (
                    "Safe file improvement completed.\n\n"
                    f"File: {result['path']}\n"
                    f"Backup: {result['backup']}"
                )
            }

        if lower.startswith("mount component "):
            component_name = (
                command
                .replace("mount component ", "", 1)
                .strip()
                .replace(" ", "")
            )

            check_component = validate_not_empty(component_name, "Component name")
            if not check_component["valid"]:
                return {"response": check_component["error"]}

            result = mount_component(component_name)

            if not result["success"]:
                log_error(result["error"])
                return {"response": f"Mount Error:\n{result['error']}"}

            log_component(component_name)

            return {
                "response": (
                    "Component mounted successfully:\n\n"
                    f"{result['component']}\n"
                    f"{result['path']}"
                )
            }

        if lower.startswith("generate component "):
            body = command.replace("generate component ", "", 1).strip()

            check = validate_contains(
                body,
                " for ",
                "generate component COMPONENT_NAME for DESCRIPTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" for ")
            component_name = body[:split_index].strip().replace(" ", "")
            instruction = body[split_index + len(" for "):].strip()

            check_component = validate_not_empty(component_name, "Component name")
            if not check_component["valid"]:
                return {"response": check_component["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            result = generate_component_files(component_name, instruction)

            log_component(component_name)

            return {
                "response": (
                    "Component generated successfully:\n\n"
                    f"Component: {result['component']}\n"
                    f"TSX: {result['tsx_path']}\n"
                    f"CSS: {result['css_path']}"
                )
            }

        if lower.startswith("generate file "):
            body = command.replace("generate file ", "", 1).strip()

            check = validate_contains(
                body,
                " for ",
                "generate file PATH for DESCRIPTION",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" for ")
            raw_path = body[:split_index].strip()
            instruction = body[split_index + len(" for "):].strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            check_instruction = validate_not_empty(instruction, "Instruction")
            if not check_instruction["valid"]:
                return {"response": check_instruction["error"]}

            path = normalize_path(raw_path)
            result = generate_file(path, instruction)

            log_file_edit(path)

            return {
                "response": (
                    f"AI generated file successfully:\n\n"
                    f"{result['path']}"
                )
            }

        if lower.startswith("read file "):
            raw_path = command.replace("read file ", "", 1).strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            path = normalize_path(raw_path)
            result = read_file(path)

            if not result["success"]:
                return {"response": f"Read File Error:\n{result['error']}"}

            return {
                "response": (
                    f"FILE READ:\n{path}\n\n"
                    f"{result['content'][:6000]}"
                )
            }

        if lower.startswith("create file "):
            raw_path = command.replace("create file ", "", 1).strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            path = normalize_path(raw_path)
            create_file(path, "")

            log_file_edit(path)

            return {"response": f"File created:\n{path}"}

        if lower.startswith("append file "):
            body = command.replace("append file ", "", 1).strip()

            check = validate_contains(
                body,
                " content ",
                "append file PATH content TEXT",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = body.lower().index(" content ")
            raw_path = body[:split_index].strip()
            content = body[split_index + len(" content "):]

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            check_content = validate_not_empty(content, "Content")
            if not check_content["valid"]:
                return {"response": check_content["error"]}

            path = normalize_path(raw_path)
            append_file(path, content)

            log_file_edit(path)

            return {"response": f"Content appended:\n{path}"}

        if lower.startswith("delete file "):
            raw_path = command.replace("delete file ", "", 1).strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            path = normalize_path(raw_path)
            delete_file(path)

            log_file_edit(path)

            return {"response": f"File deleted:\n{path}"}

        if lower.startswith("list files in "):
            raw_path = command.replace("list files in ", "", 1).strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            path = normalize_path(raw_path)
            result = list_project_files(path)

            if not result["success"]:
                return {"response": f"List Files Error:\n{result['error']}"}

            files = result["files"][:100]
            text = "\n".join([f"- {file}" for file in files])

            return {
                "response": (
                    f"FILES IN:\n{path}\n\n"
                    f"{text}"
                )
            }

        if lower.startswith("open file "):
            raw_path = command.replace("open file ", "", 1).strip()

            check_path = validate_file_command_path(raw_path)
            if not check_path["valid"]:
                return {"response": check_path["error"]}

            path = normalize_path(raw_path)

            subprocess.Popen(
                ["code", path],
                shell=True,
            )

            return {"response": f"Opening file:\n{path}"}

        if lower.startswith("ask jarvis "):
            prompt = command.replace("ask jarvis ", "", 1).strip()

            check_prompt = validate_not_empty(prompt, "Prompt")
            if not check_prompt["valid"]:
                return {"response": check_prompt["error"]}

            if not conversation_mode.is_planning():
                conversation_mode.enter_planning()

            session = conversation_mode.planning_session
            session.add_exchange("user", prompt)

            context = session.get_context()

            ai_response = ask_ollama(
                f"""
{context}

USER REQUEST:
{prompt}
"""
            )

            session.add_exchange("assistant", ai_response)

            return {"response": ai_response}

        if lower == "show planning":
            if not conversation_mode.is_planning():
                return {"response": "No active planning session."}

            session = conversation_mode.planning_session

            return {"response": session.get_context()}

        if lower == "generate project plan":
            if not conversation_mode.is_planning():
                return {"response": "No active planning session."}

            session = conversation_mode.planning_session
            plan = generate_project_plan(session)

            return {"response": plan}

        if lower == "generate project files":
            if not conversation_mode.is_planning():
                return {"response": "No active planning session."}

            session = conversation_mode.planning_session
            files = generate_project_files(session)

            return {"response": files}

        if lower == "reset planning":
            conversation_mode.return_to_chat()
            return {"response": "Planning session reset."}

        if lower.startswith("build project "):
            project_name = (
                command
                .replace("build project ", "", 1)
                .strip()
                .replace(" ", "-")
                .lower()
            )

            check_project = validate_not_empty(project_name, "Project name")
            if not check_project["valid"]:
                return {"response": check_project["error"]}

            project_path = build_project_structure(project_name)

            return {
                "response": (
                    "Project structure created:\n\n"
                    f"{project_path}"
                )
            }

        if lower.startswith("open project "):
            project_name = command.replace("open project ", "", 1).strip()

            check_project = validate_not_empty(project_name, "Project name")
            if not check_project["valid"]:
                return {"response": check_project["error"]}

            project_path = open_generated_project(project_name)

            if project_path:
                return {
                    "response": (
                        f"Opening project:\n\n"
                        f"{project_path}"
                    )
                }

            return {
                "response": (
                    f"Project not found:\n\n"
                    f"{project_name}"
                )
            }

        if lower.startswith("run task "):
            task_body = command.replace("run task ", "", 1).strip()

            check = validate_contains(
                task_body,
                " command ",
                "run task TASK_NAME command COMMAND_HERE",
            )

            if not check["valid"]:
                return {"response": check["error"]}

            split_index = task_body.lower().index(" command ")
            task_name = task_body[:split_index].strip().replace(" ", "-").lower()
            task_command = task_body[split_index + len(" command "):].strip()

            check_task = validate_not_empty(task_name, "Task name")
            if not check_task["valid"]:
                return {"response": check_task["error"]}

            check_command = validate_not_empty(task_command, "Task command")
            if not check_command["valid"]:
                return {"response": check_command["error"]}

            if is_blocked_task(task_command):
                return {
                    "response": (
                        "Task blocked for safety.\n\n"
                        "This command contains a dangerous system action."
                    )
                }

            result = task_engine.execute(task_name, task_command)

            log_task(task_name)

            if result["success"]:
                return {
                    "response": (
                        f"Task completed: {result['task']}\n\n"
                        f"Output:\n{result['output']}\n\n"
                        f"Log saved:\n{result['log']}"
                    )
                }

            log_error(
                result.get(
                    "error",
                    result.get("output", "Unknown task failure.")
                )
            )

            return {
                "response": (
                    f"Task failed: {result['task']}\n\n"
                    f"Error:\n"
                    f"{result.get('error', result.get('output', 'Unknown task failure.'))}"
                )
            }

        if lower == "show tasks":
            logs = list_task_logs()

            if not logs:
                return {"response": "No task logs found yet."}

            text = "\n".join([
                f"- {item['name']}\n  {item['path']}"
                for item in logs[:10]
            ])

            return {
                "response": f"Recent task logs:\n\n{text}"
            }

        if lower.startswith("read task "):
            task_name = (
                command
                .replace("read task ", "", 1)
                .strip()
                .replace(" ", "-")
                .lower()
            )

            check_task = validate_not_empty(task_name, "Task name")
            if not check_task["valid"]:
                return {"response": check_task["error"]}

            content = read_task_log(task_name)

            if content is None:
                return {"response": f"No task log found for:\n{task_name}"}

            return {
                "response": (
                    f"Task log for {task_name}:\n\n"
                    f"{content[:4000]}"
                )
            }


        if lower.startswith("remember jarvis memory "):
            body = command.replace(
                "remember jarvis memory ",
                "",
                1
            ).strip()

            check = validate_contains(
                body,
                " content ",
                "remember jarvis memory CATEGORY content TEXT",
            )

            if not check["valid"]:
                return {
                    "response": check["error"]
                }

            split_index = body.lower().index(" content ")

            category = body[:split_index].strip()

            content = body[
                split_index + len(" content "):
            ].strip()

            result = save_memory(
                category,
                content,
            )

            return {
                "response": format_memory_saved(result)
            }

        if lower in [
            "show jarvis memory",
            "jarvis memory",
            "show memory",
        ]:
            result = list_memories()

            return {
                "response": format_memory_list(result)
            }

        if lower.startswith("search jarvis memory "):
            query = command.replace(
                "search jarvis memory ",
                "",
                1
            ).strip()

            result = search_memories(query)

            return {
                "response": format_memory_search(result)
            }

        if lower in [
            "memory summary",
            "summarize memory",
        ]:
            result = summarize_memory()

            return {
                "response": format_memory_summary(result)
            }

        if lower in [
            "recent conversation memory",
            "show conversation memory",
        ]:
            result = get_recent_conversation()

            return {
                "response": format_recent_conversation(result)
            }

        if lower.startswith("search conversation memory "):
            query = command.replace(
                "search conversation memory ",
                "",
                1
            ).strip()

            result = search_conversation(query)

            return {
                "response": format_conversation_search(result)
            }

        if lower in [
            "show project state",
            "project state",
            "current phase",
        ]:
            result = get_project_state()

            return {
                "response": format_project_state(result)
            }

        if lower.startswith("set project phase "):
            phase = command.replace(
                "set project phase ",
                "",
                1
            ).strip()

            result = update_project_state(
                "current_phase",
                phase,
            )

            return {
                "response": format_project_state(result)
            }

        if lower.startswith("remember project blocker "):
            blocker = command.replace(
                "remember project blocker ",
                "",
                1
            ).strip()

            result = add_project_blocker(
                blocker
            )

            return {
                "response": format_project_state(result)
            }


        if lower.startswith("remember "):
            memory_text = command.replace("remember ", "", 1).strip()

            check_memory = validate_not_empty(memory_text, "Memory")
            if not check_memory["valid"]:
                return {"response": check_memory["error"]}

            db = SessionLocal()

            memory = Memory(
                category="general",
                content=memory_text,
            )

            db.add(memory)
            db.commit()
            db.close()

            return {
                "response": f"Memory saved:\n\n{memory_text}"
            }

        if lower == "show memories":
            db = SessionLocal()
            memories = db.query(Memory).all()
            db.close()

            if not memories:
                return {"response": "No memories stored."}

            memory_text = "\n".join([
                f"- {memory.content}"
                for memory in memories
            ])

            return {
                "response": f"Stored memories:\n\n{memory_text}"
            }

        for app_name, target in APP_COMMANDS.items():
            if app_name in lower:
                subprocess.Popen(
                    ["cmd", "/c", "start", "", target],
                    shell=True,
                )

                return {"response": f"Opening {app_name}"}

        for site_name, url in WEBSITE_COMMANDS.items():
            if site_name in lower:
                webbrowser.open(url)

                return {"response": f"Opening {site_name}"}

        for phrase, terminal_command in SAFE_TERMINAL_COMMANDS.items():
            if phrase in lower:
                output = run_shell(terminal_command)

                return {"response": output}

        return {"response": "Command not recognized."}

    except Exception as e:
        log_error(str(e))

        return {
            "response": (
                f"JARVIS ERROR:\n{str(e)}"
            )
        }
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )  
