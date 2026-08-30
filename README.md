# 🧹 Digital Declutter Agent

An AI-powered digital decluttering assistant that investigates messy folders, finds duplicates, reads relevant files, and provides cleanup and naming recommendations.

## 💡 The Problem

Over time, our computers accumulate documents, PDFs, images, duplicate files, and poorly named files.

Traditional file organizers can sort files based on extensions, but they cannot easily answer questions such as:

- What is this document about?
- Which files are duplicates?
- Which files are relevant?
- Is this filename meaningful?
- What would be a better name for this file?

The Digital Declutter Agent uses an AI agent to inspect files, understand relevant content, identify duplicates, and suggest useful cleanup and naming improvements.

## 🤖 What the Agent Can Do

The agent can:

- Recursively inspect directories
- Gather basic file information
- Identify duplicate files using SHA-256 hashes
- Read supported text files
- Extract text from PDF files
- Read JPEG, PNG, and WebP images through MCP `ImageContent`
- Summarize relevant documents
- Suggest more descriptive filenames
- Follow user instructions such as "Do not modify anything"

The current prototype focuses on **inspection, understanding, and recommendations**. It does not automatically rename, move, or delete files.

## 🏗️ Architecture

```text
                         User
                           │
                           ▼
                    TrueForge Agent
                           │
                    Agent reasoning
                           │
                           ▼
                      MCP Server
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   scan_directory   find_duplicate_files   read_file
                                             │
                              ┌──────────────┼──────────────┐
                              │              │              │
                              ▼              ▼              ▼
                            Text            PDF           Image
                           Reader          Reader         Reader
                              │              │              │
                              └──────────────┼──────────────┘
                                             │
                                             ▼
                                    Agent analyzes results
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                         Summaries      Duplicate      Rename
                                         findings      suggestions
```

## 🔧 MCP Tools

### `scan_directory`

Recursively scans a directory and returns basic information about the files it discovers, including:

- Filename
- Relative path
- File extension
- File size

### `find_duplicate_files`

Finds files with identical contents.

The implementation first groups files by size and then calculates SHA-256 hashes for candidate files to identify exact duplicates.

### `read_file`

Provides a unified interface for reading supported file types.

The reader routes files to format-specific implementations:

```text
read_file()
    │
    ├── Text → Text Reader
    ├── PDF  → PDF Reader
    └── Image → Image Reader
```

## 📄 Supported File Types

The unified `read_file` tool supports multiple file formats through dedicated readers.

### Text Files

Supported text files are read as text content with a resource-size safeguard.

### PDF Files

PDF files are processed using `pypdf`.

The PDF reader applies limits to:

- PDF file size
- Number of pages
- Extracted text size

These limits help prevent excessively large documents from consuming unbounded resources.

### Image Files

The image reader currently supports:

- JPEG
- PNG
- WebP

Images are returned as MCP `ImageContent` with base64-encoded image data.

Image files also have a maximum file-size limit.

## 🔐 Safety & Security

Filesystem access is treated as a security boundary.

The MCP server validates requested files against an explicitly supplied allowed root before reading them.

The readers also use resource limits to prevent unexpectedly large files from consuming excessive memory.

### Secure File Access

The image reader uses a validated file descriptor for reading rather than repeatedly opening the file by pathname.

It also uses:

- `O_NOFOLLOW` to help prevent symlink-based escapes
- `fstat()` to inspect the opened file
- bounded reads to enforce the image-size limit
- reliable file-descriptor cleanup

These measures help protect the filesystem boundary and prevent resource-exhaustion issues.

### Security Review with Qodo

During development, Qodo identified a high-severity path-race vulnerability in the image reader.

The original implementation validated the pathname, checked its size, and then opened it separately for reading. This could allow a file to be replaced between those operations.

The issue was fixed by using a single validated file descriptor for the subsequent size check and read.

The fix was then reviewed again by Qodo.

## 🧠 TrueForge Agent

The MCP tools are connected to an agent running through TrueForge.

TrueForge provides the agent orchestration and reasoning layer, while the MCP server provides the filesystem capabilities.

For example, the agent was given the request:

> Inspect `test_data`, find duplicates, and read relevant documents. Do not modify, rename, move, or delete anything.

The agent independently selected and used the available MCP tools to:

1. Inspect the directory
2. Identify duplicate files
3. Select relevant documents
4. Read their contents
5. Summarize the information
6. Suggest more descriptive filenames

The agent was also able to inspect a folder containing Operations Management PDFs, read the relevant documents, and produce concise summaries of their contents.

### Agent Workflow

```text
User Request
     ↓
TrueForge Agent
     ↓
Agent Reasoning
     ↓
Select MCP Tools
     ↓
┌─────────────────────────────┐
│ scan_directory              │
│ find_duplicate_files        │
│ read_file                   │
└─────────────────────────────┘
     ↓
Inspect & Understand Files
     ↓
Agent Reasoning
     ↓
┌─────────────────────────────┐
│ Summaries                   │
│ Duplicate Findings          │
│ Rename Suggestions          │
└─────────────────────────────┘
```

## 🔎 Qodo Code Review Evidence

Qodo was integrated into the development workflow and used to review
substantive changes through pull requests.

### Development PRs

- **PR #1 — Duplicate Detection:** Added duplicate-file detection using file-content hashing.
- **PR #2 — Read File:** Added the MCP `read_file` tool and hardened
  file access with security and size-limit checks.
- **PR #3 — PDF Reader:** Added PDF reading support with resource limits.
- **PR #4 — Image Reader:** Added image support and underwent Qodo
  security review.

### Representative Qodo-reviewed PR

**PR #4 — Image Reader**

During this review, Qodo identified a high-severity path-race
vulnerability in the image reader. The issue was fixed using secure
file-descriptor handling and bounded reads.

The fix was subsequently reviewed again by Qodo.

**Final Qodo Review:**

- 🐞 Bugs: **0**
- 📘 Rule violations: **0**
- 📜 Skill insights: **0**

[PR #4 — Add image file support](https://github.com/evangelin-blessy-hk/digital-declutter-agent/pull/4)

## 🚀 Running the MCP Server

### 1. Clone the repository

```bash
git clone https://github.com/evangelin-blessy-hk/digital-declutter-agent.git
cd digital-declutter-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Linux / WSL:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the MCP server

```bash
python -m mcp_server.server
```

The MCP server runs locally using Streamable HTTP at:

```text
http://127.0.0.1:8000
```

### 6. Connect the MCP server to TrueForge

Configure the MCP server in TrueForge using the local server endpoint.

The agent can then access these MCP tools:

- `scan_directory`
- `find_duplicate_files`
- `read_file`

These tools allow the TrueForge agent to inspect directories, identify duplicates, and read supported files.

## 🧪 Example Agent Usage

The agent can inspect a folder and decide which MCP tools are relevant to the user's request.

### Example 1: Folder Inspection and Duplicate Detection

**User request:**

> Inspect `test_data`, find duplicates, and read relevant documents. Do not modify, rename, move, or delete anything.

The agent inspected the directory and identified an exact duplicate pair:

```text
test_data/Documents_AFO/file1.txt
test_data/Documents_AFO/file2.txt
```

Both files contained the same content.

The agent also read relevant documents and provided summaries and filename recommendations.

### Example 2: PDF Analysis

**User request:**

> Inspect `test_data/Documents/operations management IIMB`. Identify the available documents, read the relevant PDFs, and give me a concise summary of what they contain. Do not modify anything.

The agent identified:

```text
Week_1_handout.pdf
Week_2_handout.pdf
```

It then read the PDFs and summarized their contents, including topics such as:

- Operations management fundamentals
- Operations systems and flow
- Continuous, intermittent, and jumbled flow
- Performance metrics
- Service operations
- Make-to-order operations
- Specialized workforce and service variety

### Example 3: Filename Recommendations

After understanding file contents, the agent can provide more descriptive filename suggestions.

For example:

```text
Week_1_handout.pdf
    ↓
IIMB_OM_Week01_Introduction_to_Operations.pdf

Week_2_handout.pdf
    ↓
IIMB_OM_Week02_Service_Operations.pdf
```

These are recommendations only. The current demonstrated workflow does not automatically rename files.

### Agent Decision Flow

```text
User Request
     ↓
TrueForge Agent
     ↓
Determine relevant information
     ↓
Select MCP tools
     ↓
Inspect / Read files
     ↓
Reason over results
     ↓
Return useful recommendations
```

The agent therefore acts as a reasoning layer over the filesystem tools rather than simply executing a predefined sequence of file operations.

## 🔮 Future Improvements

The current prototype focuses on safe file inspection, understanding, and recommendations.

Future versions could introduce:

- User-approved file renaming
- Safe file moving
- User-approved duplicate cleanup
- Protected system and application paths
- Richer image understanding
- Storage usage analysis
- Dry-run cleanup plans
- Audit history for applied changes

The long-term workflow is:

```text
Investigate
    ↓
Understand
    ↓
Assess
    ↓
Explain
    ↓
Ask for permission
    ↓
Perform approved actions
    ↓
Report
```

The goal is to keep the agent's reasoning separate from filesystem actions so that potentially destructive operations require explicit user approval.