"""
SUPER MASTER AI COMMAND GENERATOR — ALL IN ONE FILE
=====================================================
Target  : 70 Lakh+ commands from 6500+ topics
Model   : mistralai/Mistral-7B-Instruct-v0.3
Keys    : HF_KEY_A and HF_KEY_B with auto-rotation
Rotation: A runs → A limit hit → B runs →
          B limit hit → A runs → repeat forever
Schedule: 24/7 continuous via GitHub Actions
Resume  : Auto-resume from checkpoint on every run

PROJECT SPECIFICATION (System Instructions):
============================================
Objective: High-Volume Automated AI Command Generation
           (70 Lakh+ Scale)

1. SCOPE — IN:
   - AI-driven content creation logic
   - Technical commands for workflow automation
   - Content asset generation up to Google Drive stage

2. SCOPE — OUT (STRICTLY EXCLUDED):
   - YouTube uploading or video management
   - YouTube SEO or any SEO strategy
   - Digital marketing or platform publishing
   - Video promotion or link building
   - Channel analytics or monetization strategy

3. GENERATION PROTOCOL:
   - Minimum 1000 unique commands per topic
   - 100% accuracy, professional, actionable
   - Continuous non-stop execution loop
   - API key A/B rotation for zero downtime

4. QUALITY STANDARD (1000 Code Guidelines Summary):
   - 4 spaces indentation, max 79 chars per line
   - snake_case functions, PascalCase classes
   - UPPER_CASE constants, type hints everywhere
   - Google-style docstrings on all public methods
   - No bare except, always catch specific exceptions
   - Structured logging, never print statements
   - Single Responsibility Principle enforced
   - Dependency injection over hardcoding
   - Pydantic/dataclass for all data structures
   - Atomic checkpoint writes to prevent corruption
   - Exponential backoff on all API retries
   - Thread-safe resource management
   - No secrets in code, use environment variables
   - Pathlib for all file system operations
   - Context managers for all resources
"""

# ============================================================
# AUTO DEPENDENCY INSTALLER
# ============================================================
import subprocess
import sys


def _install_missing_deps() -> None:
    """Install required packages if not already present."""
    required = ["requests"]
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install",
                 package, "--quiet"],
                stdout=subprocess.DEVNULL,
            )


_install_missing_deps()


# ============================================================
# STANDARD IMPORTS
# ============================================================
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


import requests


# ============================================================
# CONFIGURATION — Only edit HF_KEY_A and HF_KEY_B
# ============================================================
GOOGLE_DOC_ID: str = (
    "1EG4YzCD2uCbWSWRxCO8kX4mySTnEEbvnas40VsLz17A"
)
GOOGLE_DOC_URL: str = (
    f"https://docs.google.com/document/d/{GOOGLE_DOC_ID}"
    f"/export?format=txt"
)
GOOGLE_DOC_URL_HTML: str = (
    f"https://docs.google.com/document/d/{GOOGLE_DOC_ID}"
    f"/export?format=html"
)
GOOGLE_DOC_URL_PUB: str = (
    f"https://docs.google.com/document/d/{GOOGLE_DOC_ID}"
    f"/pub?output=txt"
)

# ✏️ ADD YOUR KEYS HERE OR SET AS ENVIRONMENT VARIABLES
HF_KEY_A: str = os.environ.get("HF_KEY_A", "hf_ADD_KEY_A_HERE")
HF_KEY_B: str = os.environ.get("HF_KEY_B", "hf_ADD_KEY_B_HERE")


# Best free models on HuggingFace — tries in order
# Falls back to next if one fails or is overloaded
HF_MODELS: List[str] = [
    "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Best free
    "meta-llama/Llama-3.1-8B-Instruct",       # 2nd best
    "mistralai/Mistral-7B-Instruct-v0.3",     # Fallback
]
HF_MODEL: str = HF_MODELS[0]
HF_API_URL: str = (
    f"https://api-inference.huggingface.co/models/{HF_MODEL}"
)

COMMANDS_PER_TOPIC: int = 1000
OUTPUT_DIR: Path = Path("output")
CHECKPOINT_FILE: Path = Path("checkpoint.json")
LOG_FILE: Path = Path("generator.log")

REQUEST_DELAY_SEC: float = 3.0
MAX_RETRIES: int = 6
BACKOFF_BASE_SEC: int = 15

# Safe exit at 5 hours = 300 minutes
# GitHub kills at 5.5h so we exit at 5h safely
MAX_RUN_SECONDS: int = 300 * 60

# Commit progress to repo every N topics
COMMIT_EVERY_N_TOPICS: int = 10


# ============================================================
# EXCLUDED TOPIC KEYWORDS — YT/SEO/Upload ❌
# ============================================================
EXCLUDED_KEYWORDS: List[str] = [
    "youtube seo",
    "video seo",
    "seo strategy",
    "search engine optimization",
    "youtube upload",
    "video upload",
    "upload schedule",
    "upload automation",
    "youtube algorithm",
    "youtube studio",
    "channel management",
    "channel growth",
    "video promotion",
    "youtube marketing",
    "video marketing",
    "digital marketing",
    "subscriber growth",
    "youtube analytics",
    "channel analytics",
    "video monetization",
    "youtube monetization",
    "adsense",
    "youtube ads",
    "video distribution",
    "platform publishing",
    "link building",
    "youtube ranking",
    "video ranking",
    "keyword research youtube",
    "youtube keyword",
    "video tags",
    "youtube tags",
    "youtube description seo",
    "video description seo",
    "thumbnail seo",
    "click through rate",
    "youtube ctr",
    "watch time optimization",
    "youtube watch time",
    "shorts strategy",
    "reels strategy",
    "tiktok strategy",
    "social media marketing",
    "influencer marketing",
    "brand deals",
    "sponsorship youtube",
    "youtube partnership",
    "content calendar youtube",
    "posting schedule youtube",
]

# ============================================================
# SYSTEM PROMPT FOR AI COMMAND GENERATION
# ============================================================
SYSTEM_PROMPT: str = """
You are a world-class AI content creation automation expert.

YOUR MAIN GOAL:
Generate the MAXIMUM possible number of unique, professional,
actionable technical commands for the given topic.

QUANTITY RULES:
- Generate as many commands as you possibly can.
- Aim for 1000+ commands minimum.
- If the topic allows 5000, generate 5000.
- If the topic allows 30000, generate 30000.
- Never stop early. Always push to your absolute maximum.
- More commands = better. Quality AND quantity both matter.

QUALITY RULES:
- Every command must be unique, not repeated.
- Every command must be immediately implementable.
- Commands must be technical, specific, professional.
- Cover every possible angle of the topic deeply.
- Go from beginner to advanced to expert level.
- Cover tools, techniques, workflows, automation, settings,
  parameters, configurations, optimizations, edge cases.

STRICTLY FORBIDDEN:
- YouTube uploading or channel management
- SEO strategies or keyword optimization
- Video promotion or marketing
- Social media strategies
- YouTube analytics or monetization

FORMAT:
- Number every command starting from 1.
- One command per line.
- No explanations, just the command itself.
- Never stop until you have exhausted every possibility.
"""


# ============================================================
# LOGGER SETUP
# ============================================================
def _setup_logger() -> logging.Logger:
    """
    Configure structured logger with file and console.

    Returns:
        Configured Logger instance.
    """
    log_formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | %(levelname)-8s | "
            "%(filename)s:%(lineno)d | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("master_gen")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(
            LOG_FILE, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


LOGGER = _setup_logger()


# ============================================================
# DATA STRUCTURES
# ============================================================
@dataclass
class Checkpoint:
    """
    Tracks generation progress for full resume support.

    Attributes:
        completed_topics: Topics already processed.
        total_commands: Total commands generated so far.
        current_key_index: Active API key index (0 or 1).
        approved_topics: Filtered topic list.
        excluded_topics: Topics removed from processing.
        topics_loaded: Whether doc was already parsed.
    """

    completed_topics: List[str] = field(default_factory=list)
    total_commands: int = 0
    current_key_index: int = 0
    approved_topics: List[str] = field(default_factory=list)
    excluded_topics: List[str] = field(default_factory=list)
    topics_loaded: bool = False


# ============================================================
# CHECKPOINT HELPERS
# ============================================================
def load_checkpoint() -> Checkpoint:
    """
    Load checkpoint from disk or return fresh instance.

    Returns:
        Checkpoint with saved progress or empty default.
    """
    if CHECKPOINT_FILE.exists():
        try:
            with open(
                CHECKPOINT_FILE, "r", encoding="utf-8"
            ) as chk_file:
                data = json.load(chk_file)
            LOGGER.info("✅ Checkpoint loaded — resuming.")
            return Checkpoint(**data)
        except (json.JSONDecodeError, TypeError) as error:
            LOGGER.warning(
                f"Checkpoint corrupt, restarting: {error}"
            )
    return Checkpoint()


def save_checkpoint(checkpoint: Checkpoint) -> None:
    """
    Atomically persist checkpoint to prevent corruption.

    Args:
        checkpoint: Current progress state to save.
    """
    tmp_path = CHECKPOINT_FILE.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as chk:
            json.dump(checkpoint.__dict__, chk, indent=2)
        tmp_path.replace(CHECKPOINT_FILE)
    except OSError as error:
        LOGGER.error(f"Checkpoint save failed: {error}")


# ============================================================
# GOOGLE DOC READER
# ============================================================
def fetch_google_doc() -> str:
    """
    Stream-download Google Doc with retries and fallbacks.

    Tries 3 different URL formats to maximize success.
    Uses streaming to handle very large documents safely.

    Returns:
        Full document text string.

    Raises:
        RuntimeError: When all retry attempts are exhausted.
    """
    url_variants: List[str] = [
        GOOGLE_DOC_URL,
        GOOGLE_DOC_URL_HTML,
        GOOGLE_DOC_URL_PUB,
    ]

    for attempt in range(1, MAX_RETRIES + 1):
        for url in url_variants:
            try:
                LOGGER.info(
                    f"📥 Fetching doc attempt {attempt}..."
                )
                chunks: List[str] = []
                with requests.get(
                    url,
                    timeout=180,
                    stream=True,
                ) as response:
                    response.raise_for_status()
                    for chunk in response.iter_content(
                        chunk_size=65536,
                        decode_unicode=True,
                    ):
                        if chunk:
                            chunks.append(chunk)

                full_text = "".join(chunks)
                LOGGER.info(
                    f"✅ Doc fetched: {len(full_text):,} chars."
                )
                return full_text

            except requests.Timeout:
                LOGGER.warning(f"⏱ Timeout attempt {attempt}.")
            except requests.HTTPError as error:
                LOGGER.warning(f"HTTP error: {error}")
            except requests.RequestException as error:
                LOGGER.warning(f"Request failed: {error}")

        wait_sec = BACKOFF_BASE_SEC * attempt
        LOGGER.info(f"Waiting {wait_sec}s before retry...")
        time.sleep(wait_sec)

    raise RuntimeError(
        "❌ Failed to fetch Google Doc after all attempts."
        " Ensure document is set to 'Anyone with link'."
    )


def extract_topics(raw_text: str) -> List[str]:
    """
    Parse numbered topic list from raw document text.

    Args:
        raw_text: Full Google Doc content as string.

    Returns:
        List of clean topic strings.
    """
    pattern = re.compile(
        r"^\s*\d+[\.\)]\s+(.+)$",
        re.MULTILINE,
    )
    topics = [
        match.strip()
        for match in pattern.findall(raw_text)
        if match.strip()
    ]
    LOGGER.info(f"📋 Extracted {len(topics)} raw topics.")
    return topics


def is_excluded(topic: str) -> bool:
    """
    Check if a topic matches any excluded keyword.

    Args:
        topic: Topic string to evaluate.

    Returns:
        True if topic should be skipped.
    """
    topic_lower = topic.lower()
    return any(kw in topic_lower for kw in EXCLUDED_KEYWORDS)


def filter_topics(
    topics: List[str],
) -> Tuple[List[str], List[str]]:
    """
    Separate topics into approved and excluded lists.

    Args:
        topics: All extracted topic strings.

    Returns:
        Tuple of (approved_topics, excluded_topics).
    """
    approved: List[str] = []
    excluded: List[str] = []
    for topic in topics:
        if is_excluded(topic):
            excluded.append(topic)
        else:
            approved.append(topic)
    LOGGER.info(
        f"✅ Approved: {len(approved)} | "
        f"❌ Excluded: {len(excluded)}"
    )
    return approved, excluded


def save_excluded_audit(excluded_topics: List[str]) -> None:
    """
    Write excluded topics audit trail to disk.

    Args:
        excluded_topics: List of filtered-out topics.
    """
    audit_path = OUTPUT_DIR / "excluded_audit.txt"
    with open(audit_path, "w", encoding="utf-8") as audit:
        audit.write(
            "EXCLUDED TOPICS AUDIT — YT/SEO/Upload\n"
        )
        audit.write("=" * 50 + "\n\n")
        for idx, topic in enumerate(excluded_topics, start=1):
            audit.write(f"{idx}. {topic}\n")
    LOGGER.info(f"📝 Audit saved: {audit_path}")


# ============================================================
# API KEY ROTATOR — A → B → A → B (Infinite Loop)
# ============================================================
class ApiKeyRotator:
    """
    Manages automatic A/B rotation between HF API keys.

    Rotation logic:
        KEY_A runs → rate limit hit → switch to KEY_B
        KEY_B runs → rate limit hit → switch to KEY_A
        This loop repeats forever until all topics done.

    Attributes:
        _keys: List of two HuggingFace API key strings.
        _index: Index of currently active key (0 or 1).
    """

    def __init__(
        self,
        key_a: str,
        key_b: str,
        start_index: int = 0,
    ) -> None:
        self._keys: List[str] = [key_a, key_b]
        self._index: int = start_index

    @property
    def current_key(self) -> str:
        """Return the currently active API key."""
        return self._keys[self._index]

    @property
    def current_index(self) -> int:
        """Return index of current key for checkpointing."""
        return self._index

    @property
    def key_label(self) -> str:
        """Return human-readable label of current key."""
        return f"KEY_{'A' if self._index == 0 else 'B'}"

    def rotate(self) -> None:
        """
        Switch to the next API key in rotation.

        KEY_A (0) → KEY_B (1) → KEY_A (0) → ...
        """
        previous = self.key_label
        self._index = (self._index + 1) % len(self._keys)
        LOGGER.warning(
            f"🔄 Key rotated: {previous} → {self.key_label}"
        )


# ============================================================
# PROMPT BUILDER
# ============================================================
def build_prompt(topic: str) -> str:
    """
    Build HuggingFace instruction prompt for one topic.

    Instructs AI to generate maximum possible commands,
    not a fixed number. Quality and quantity both matter.

    Args:
        topic: The topic to generate commands for.

    Returns:
        Formatted Mistral instruction prompt string.
    """
    return (
        f"<s>[INST] {SYSTEM_PROMPT}\n\n"
        f"TOPIC: {topic}\n\n"
        f"Generate the MAXIMUM number of unique, technical,"
        f" professional AI content creation commands for this"
        f" topic. Aim for 1000+ but go as high as possible."
        f" If you can do 5000 or 10000, do it."
        f" Cover every tool, technique, workflow, setting,"
        f" parameter, configuration, and edge case.\n\n"
        f"Start from 1 and go until you have exhausted"
        f" every single possibility for this topic."
        f" Never stop early. [/INST]"
    )


# ============================================================
# HF API CALLER
# ============================================================
def call_hf_api(
    prompt: str,
    rotator: ApiKeyRotator,
) -> Optional[str]:
    """
    Call HuggingFace API with retry, rotation, model fallback.

    Tries best model first, falls back to next on failure.
    On rate limit (429): rotates to other key instantly.
    On model loading (503): waits 30s then retries.

    Args:
        prompt: Formatted instruction prompt string.
        rotator: ApiKeyRotator instance for key management.

    Returns:
        Generated command text or None if all retries fail.
    """
    for model in HF_MODELS:
        api_url = (
            f"https://api-inference.huggingface.co"
            f"/models/{model}"
        )
        LOGGER.info(f"🤖 Trying model: {model.split('/')[1]}")

        for attempt in range(1, MAX_RETRIES + 1):
            headers = {
                "Authorization": (
                    f"Bearer {rotator.current_key}"
                ),
                "Content-Type": "application/json",
            }
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 8192,
                    "temperature": 0.9,
                    "return_full_text": False,
                    "do_sample": True,
                    "repetition_penalty": 1.1,
                },
            }

            try:
                LOGGER.debug(
                    f"Attempt {attempt}/{MAX_RETRIES} "
                    f"via {rotator.key_label}"
                )
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and result:
                        text = result[0].get(
                            "generated_text", ""
                        )
                        return text
                    return str(result)

                if response.status_code == 429:
                    LOGGER.warning(
                        f"⚠️ Rate limit on "
                        f"{rotator.key_label}. Rotating..."
                    )
                    rotator.rotate()
                    wait = BACKOFF_BASE_SEC * attempt
                    time.sleep(wait)
                    continue

                if response.status_code == 503:
                    LOGGER.warning(
                        "⏳ Model loading. Waiting 30s..."
                    )
                    time.sleep(30)
                    continue

                LOGGER.error(
                    f"API {response.status_code}: "
                    f"{response.text[:100]}"
                )
                time.sleep(BACKOFF_BASE_SEC * attempt)

            except requests.Timeout:
                LOGGER.warning(
                    f"⏱ Timeout attempt {attempt}."
                )
                time.sleep(BACKOFF_BASE_SEC * attempt)
            except requests.RequestException as error:
                LOGGER.exception(f"Request error: {error}")
                time.sleep(BACKOFF_BASE_SEC * attempt)

        LOGGER.warning(
            f"Model {model} exhausted. Trying next..."
        )

    LOGGER.error("❌ All models and retries exhausted.")
    return None


# ============================================================
# OUTPUT WRITER
# ============================================================
def save_commands(
    topic: str,
    topic_index: int,
    commands_text: str,
) -> Path:
    """
    Save generated commands for one topic to disk.

    Groups output into batch folders of 100 topics each.

    Args:
        topic: Topic name used for filename.
        topic_index: Sequential number for ordering.
        commands_text: Raw generated text to save.

    Returns:
        Path to saved output file.
    """
    batch_num = ((topic_index - 1) // 100) + 1
    batch_dir = OUTPUT_DIR / f"batch_{batch_num:03d}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^\w\s-]", "", topic)[:50]
    safe_name = re.sub(r"\s+", "_", safe_name).lower()
    filename = f"{topic_index:04d}_{safe_name}.txt"
    output_path = batch_dir / filename

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(f"TOPIC: {topic}\n")
        out_file.write("=" * 60 + "\n\n")
        out_file.write(commands_text)
        out_file.write("\n")

    return output_path


def count_commands(text: str) -> int:
    """
    Count numbered commands in generated text.

    Args:
        text: Generated output text to scan.

    Returns:
        Number of numbered commands found.
    """
    pattern = re.compile(r"^\s*\d+[\.\)]\s+", re.MULTILINE)
    return len(pattern.findall(text))


# ============================================================
# PROGRESS DISPLAY
# ============================================================
def show_progress(
    completed: int,
    total: int,
    total_commands: int,
    elapsed_hours: float,
) -> None:
    """
    Print visual progress bar and stats to console.

    Args:
        completed: Topics completed so far.
        total: Total approved topics.
        total_commands: Total commands generated.
        elapsed_hours: Hours elapsed this run.
    """
    pct = (completed / total * 100) if total > 0 else 0.0
    filled = int(pct / 2)
    bar = "█" * filled + "░" * (50 - filled)
    remaining = total - completed
    LOGGER.info(
        f"\n"
        f"  [{bar}] {pct:.1f}%\n"
        f"  Topics  : {completed}/{total} "
        f"({remaining} remaining)\n"
        f"  Commands: {total_commands:,}\n"
        f"  Elapsed : {elapsed_hours:.1f}h"
    )


# ============================================================
# GITHUB ACTIONS WORKFLOW WRITER
# ============================================================
def write_github_workflow() -> None:
    """
    Auto-create GitHub Actions workflow file if missing.

    This enables 24/7 auto-run without manual setup.
    Runs every hour, commits output back to repository.
    """
    workflow_dir = Path(".github/workflows")
    workflow_path = workflow_dir / "generate.yml"

    if workflow_path.exists():
        return

    workflow_dir.mkdir(parents=True, exist_ok=True)

    workflow_content = """\
name: Super Master Command Generator 24/7

on:
  workflow_dispatch:
  schedule:
    - cron: "0 * * * *"

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 330
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run Generator
        run: python master_command_generator.py
        env:
          HF_KEY_A: ${{ secrets.HF_KEY_A }}
          HF_KEY_B: ${{ secrets.HF_KEY_B }}
      - name: Commit Output
        run: |
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"
          git add output/ checkpoint.json generator.log \\
            .github/ 2>/dev/null || true
          git diff --staged --quiet || git commit -m \\
            "Auto: commands batch [$(date +'%Y-%m-%d %H:%M')]"
          git push origin main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

    with open(workflow_path, "w", encoding="utf-8") as wf:
        wf.write(workflow_content)

    LOGGER.info(
        "✅ GitHub Actions workflow created automatically!"
    )



def commit_progress_to_git(message: str) -> None:
    """
    Incrementally commit and push data to GitHub.

    Called every 10 topics so data is never lost
    even if GitHub Actions kills the job suddenly.

    Args:
        message: Git commit message string.
    """
    try:
        subprocess.run(
            ["git", "config", "user.name", "GeneratorBot"],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "bot@bot.com"],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "add", "-A"],
            check=True, capture_output=True,
        )
        staged = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            capture_output=True,
        )
        if staged.returncode == 1:
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "push", "origin", "main"],
                check=True, capture_output=True,
            )
            LOGGER.info(f"✅ Git commit: {message[:60]}")
        else:
            LOGGER.debug("Nothing to commit.")
    except subprocess.CalledProcessError as error:
        LOGGER.warning(f"Git skipped: {error}")


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================
def run() -> None:
    """
    Smart 24/7 orchestrator with graceful exit at 5 hours.

    Time management:
        - Tracks elapsed seconds since script started
        - Breaks loop safely at 300 minutes (5 hours)
        - Commits all data before sys.exit(0)
        - Next run resumes from exact checkpoint

    Checkpoint strategy:
        - Saves after EVERY single topic
        - Commits to GitHub every 10 topics
        - Final commit before clean exit
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_github_workflow()

    run_start = time.time()

    checkpoint = load_checkpoint()
    rotator = ApiKeyRotator(
        key_a=HF_KEY_A,
        key_b=HF_KEY_B,
        start_index=checkpoint.current_key_index,
    )

    LOGGER.info("=" * 60)
    LOGGER.info("SUPER MASTER AI COMMAND GENERATOR")
    LOGGER.info("SMART EXIT | INCREMENTAL CHECKPOINT")
    LOGGER.info("=" * 60)

    if not checkpoint.topics_loaded:
        LOGGER.info("Fetching topics from Google Doc...")
        raw_text = fetch_google_doc()
        all_topics = extract_topics(raw_text)
        approved, excluded = filter_topics(all_topics)
        save_excluded_audit(excluded)
        checkpoint.approved_topics = approved
        checkpoint.excluded_topics = excluded
        checkpoint.topics_loaded = True
        save_checkpoint(checkpoint)
        LOGGER.info(
            f"Approved: {len(approved)} | "
            f"Excluded: {len(excluded)}"
        )
    else:
        approved = checkpoint.approved_topics
        LOGGER.info(
            f"Resuming: {len(approved)} approved topics."
        )

    total = len(approved)
    done_before = len(checkpoint.completed_topics)
    LOGGER.info(
        f"Already done : {done_before}/{total}\n"
        f"Commands so far: {checkpoint.total_commands:,}\n"
        f"Active key   : {rotator.key_label}"
    )

    topics_this_run = 0
    graceful_exit = False

    for topic_index, topic in enumerate(approved, start=1):

        if topic in checkpoint.completed_topics:
            continue

        # SMART TIME CHECK
        elapsed_sec = time.time() - run_start
        elapsed_min = elapsed_sec / 60

        if elapsed_sec >= MAX_RUN_SECONDS:
            LOGGER.info(
                f"5h limit reached ({elapsed_min:.0f}min). "
                f"Saving and exiting cleanly..."
            )
            graceful_exit = True
            break

        if elapsed_sec >= (MAX_RUN_SECONDS - 1800):
            LOGGER.warning("30min left. Wrapping up soon...")

        LOGGER.info(
            f"[{topic_index}/{total}] "
            f"{elapsed_min:.0f}min | {topic[:55]}"
        )

        prompt = build_prompt(topic)
        result = call_hf_api(prompt, rotator)

        if not result:
            LOGGER.error(f"Skip failed: {topic[:40]}")
            continue

        cmd_count = count_commands(result)
        save_commands(topic, topic_index, result)

        # Save checkpoint after EVERY single topic
        checkpoint.completed_topics.append(topic)
        checkpoint.total_commands += cmd_count
        checkpoint.current_key_index = rotator.current_index
        save_checkpoint(checkpoint)

        topics_this_run += 1
        elapsed_h = (time.time() - run_start) / 3600
        show_progress(
            completed=len(checkpoint.completed_topics),
            total=total,
            total_commands=checkpoint.total_commands,
            elapsed_hours=elapsed_h,
        )

        # Commit to GitHub every 10 topics
        if topics_this_run % COMMIT_EVERY_N_TOPICS == 0:
            done_now = len(checkpoint.completed_topics)
            commit_progress_to_git(
                f"Auto {done_now}/{total} | "
                f"{checkpoint.total_commands:,} cmds"
            )

        time.sleep(REQUEST_DELAY_SEC)

    # Final commit before exit
    done_total = len(checkpoint.completed_topics)
    elapsed_final = (time.time() - run_start) / 3600

    LOGGER.info("=" * 60)
    LOGGER.info(
        f"Topics : {done_total}/{total} "
        f"({done_total/total*100:.1f}%)\n"
        f"Commands: {checkpoint.total_commands:,}\n"
        f"Time    : {elapsed_final:.2f}h"
    )
    LOGGER.info("=" * 60)

    if done_total >= total:
        commit_progress_to_git(
            f"COMPLETE {checkpoint.total_commands:,} commands!"
        )
        LOGGER.info("ALL TOPICS DONE!")
    else:
        commit_progress_to_git(
            f"Checkpoint {done_total}/{total} | "
            f"{checkpoint.total_commands:,} cmds | resuming"
        )
        LOGGER.info("Saved. Next run will resume.")

    sys.exit(0)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    run()
