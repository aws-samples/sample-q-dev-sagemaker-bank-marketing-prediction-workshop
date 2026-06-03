---
name: aws-drawio-diagram
description: Generate AWS architecture diagrams as draw.io XML files with proper AWS4 icons. Saves diagrams to diagrams/ and opens them via the @drawio MCP server. Use when the user asks for an AWS architecture diagram, flow chart, ML pipeline, or any diagram using AWS service shapes.
license: Apache-2.0
compatibility: Requires the @drawio MCP server (npm @drawio/mcp >= 1.2.7) connected to the agent. No Kiro-specific syntax — works in any agent that consumes agentskills.io and the @drawio MCP.
metadata:
  author: aws-samples
  version: "2.1.0"
  source-repo: sample-kiro-sagemaker-bank-marketing-prediction-workshop
---

# AWS architecture diagrams via draw.io

Use this skill when the user asks you to draw an AWS architecture diagram. It produces draw.io XML with correct AWS4 icons, saves it to `diagrams/<filename>.drawio`, and opens it via the `@drawio/mcp` server.

## When to activate

- "Draw an architecture diagram of …"
- "Create a current-state and target-state diagram for the SageMaker migration"
- "Visualize the data flow from S3 to SageMaker Processing to ModelTrainer to a real-time endpoint"
- The user explicitly types `/aws-drawio-diagram`.

## When NOT to activate

- The user asks for a Mermaid block in a markdown doc (use Mermaid directly, no MCP needed).
- The user asks for an ASCII diagram (use ASCII directly).
- The diagram has no AWS shapes (other diagram types are fine but the AWS-shape conventions in this skill don't apply).

## Workflow

1. **Clarify scope.** Ask the user what to include if unclear: source vs target, services in scope, data flow direction, decision points.
2. **Look up shapes.** Consult `references/aws-drawio-shapes.md` for the correct `resIcon` names, `fillColor` values, and style pattern. Do NOT guess shape names.
3. **Build the draw.io XML.** Use the style pattern from the reference. Every AWS icon cell MUST have `fillColor=<SERVICE_COLOR>;strokeColor=#ffffff` — never `#232F3E` for both.
4. **Save the file.** Write the XML to `diagrams/<descriptive-name>.drawio`.
5. **Open via MCP.** Call `open_drawio_xml` with the same XML content.
6. **Confirm the result.** Summarize what's in the diagram.

## Critical rules (summary — full details in references/aws-drawio-shapes.md)

- **Icons render as blank dark squares** when `fillColor=#232F3E` and `strokeColor=#232F3E`. Fix: use the AWS service category color for `fillColor` and `#ffffff` for `strokeColor`.
- **Shape names must be exact.** Common mistakes: `identity_and_access_management_iam` (wrong) vs `identity_and_access_management` (correct), `elastic_container_registry` (wrong) vs `ecr` (correct), `cloudwatch` (wrong) vs `cloudwatch_2` (correct).
- **MCP URL rendering is best-effort.** The `#create=` URL may not pre-load the AWS4 stencil library. The `.drawio` file opened directly always renders correctly. Always save the file first.

## File output convention

```
diagrams/<descriptive-name>.drawio
```

Examples: `diagrams/target-sagemaker-architecture.drawio`, `diagrams/current-state-local.drawio`

## MCP invocation

After saving the `.drawio` file, open it for immediate viewing:

```
Tool: open_drawio_xml  (from @drawio MCP)
Arguments:
  content: "<the full XML string>"
```

## Failure modes

| Symptom | Fix |
|---|---|
| All icons are blank dark squares | Use service color for `fillColor`, `#ffffff` for `strokeColor` (see reference) |
| Some icons blank, others work | Wrong `resIcon` name — check `references/aws-drawio-shapes.md` |
| Icons work in .drawio file but not via MCP URL | Known limitation; the .drawio file is the reliable artifact |
| AWS Cloud boundary missing its icon | Use `grIcon=mxgraph.aws4.group_aws_cloud_alt` |

## Reference

For the full shape catalog (1032+ shapes), color tables, style templates, edge patterns, and verified examples:

→ **`references/aws-drawio-shapes.md`**
