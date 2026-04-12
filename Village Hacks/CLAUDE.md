# Claude Code — Village Hacks Project

## Agents

The following agents are available in `.claude/agents/`. Claude Code will delegate to them automatically based on context.

| Agent | When to use |
|---|---|
| `code-reviewer` | PR reviews, pre-deploy audits, code quality checks |
| `prompt-engineer` | Designing/optimizing LLM prompts, prompt versioning, eval frameworks |
| `database-architect` | Schema design, query optimization, migrations |
| `backend-architect` | API design, system architecture, scalability decisions |
| `error-detective` | Debugging, root cause analysis, stack trace investigation |
| `api-security-audit` | Security reviews, OWASP checks, vulnerability scanning |

## Skills

### From `.claude/skills/` (this project)

| Invoke | Skill | Use for |
|---|---|---|
| `/brainstorming` | Brainstorming | Turn ideas into designs and specs before building anything |
| `/code-reviewer` | Code Reviewer | Structured code review with checklists and anti-pattern detection |
| `/frontend-design` | Frontend Design | Frontend design patterns and component structure |
| `/senior-frontend` | Senior Frontend | React patterns, Next.js optimization, component scaffolding |
| `/senior-backend` | Senior Backend | API design, DB optimization, load testing |
| `/react-best-practices` | React Best Practices | 40+ granular React rules (rendering, async, bundle, rerenders) |
| `/ui-ux-pro-max` | UI/UX Pro Max | Full UX stack data for React, Next.js, Shadcn, Tailwind, etc. |
| `/ui-design-system` | UI Design System | Design token generation and system consistency |
| `/senior-prompt-engineer` | Senior Prompt Engineer | Prompt patterns, RAG evaluation, agent orchestration |
| `/git-commit-helper` | Git Commit Helper | Conventional commit messages |
| `/senior-security` | Senior Security | OWASP, pentest guide, threat modeling |
| `/mcp-builder` | MCP Builder | MCP server scaffolding for Node & Python |

### From `~/.claude/skills/` (global)

| Invoke | Skill | Use for |
|---|---|---|
| `/prompt-optimizer` | Prompt Optimizer | Refine vague ideas → precise specs using EARS methodology |
| `/deep-research` | Deep Research | Evidence-tracked research reports with citations |
| `/product-analysis` | Product Analysis | Multi-agent parallel product audits |
| `/competitors-analysis` | Competitors Analysis | Evidence-based competitor profiling |
| `/fact-checker` | Fact Checker | Verify claims against official sources |
| `/qa-expert` | QA Expert | Test strategies following Google Testing Standards |
| `/skill-creator` | Skill Creator | Build and improve new skills |
| `/skill-reviewer` | Skill Reviewer | Validate skill quality against best practices |
| `/graphify` | Graphify | Any input → knowledge graph → HTML visualization |

## Workflow Shortcuts

**Before building anything:** `/brainstorming` → clarify requirements first  
**Writing prompts:** `/senior-prompt-engineer` or `/prompt-optimizer`  
**Code review:** `@code-reviewer` or `/code-reviewer`  
**Security check:** `@api-security-audit` or `/senior-security`  
**Research/market:** `/deep-research` → `/competitors-analysis`  
**UI work:** `/ui-ux-pro-max` + `/react-best-practices`  
**Pitch deck:** `/anthropic-skills:pptx`  
**Visual design:** `/anthropic-skills:canvas-design`
