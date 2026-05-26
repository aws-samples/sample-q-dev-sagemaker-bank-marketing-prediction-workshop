---
name: aws-drawio-diagram
description: Generate AWS architecture diagrams as draw.io (diagrams.net) XML and open them in the draw.io editor. Use when the user asks for an AWS architecture diagram, a flow chart of an ML pipeline, a target/source architecture comparison, or any AWS-shape diagram. Pairs with the @drawio MCP server's open_drawio_xml / open_drawio_csv / open_drawio_mermaid tools to render the result.
license: Apache-2.0
compatibility: Requires the @drawio MCP server (npm @drawio/mcp >= 1.2.7) connected to the agent. No Kiro-specific syntax — works in any agent that consumes agentskills.io and the @drawio MCP.
metadata:
  author: aws-samples
  version: "1.0.0"
  source-repo: sample-kiro-sagemaker-bank-marketing-prediction-workshop
---

# AWS architecture diagrams via draw.io

Use this skill when the user asks you to draw an AWS architecture diagram. It produces draw.io XML (or Mermaid) and hands it to the `@drawio/mcp` server, which renders the diagram in the editor.

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
2. **Build the draw.io XML.** Use the AWS shapes library (`shape=mxgraph.aws4.<service>`). Reference: `references/aws-drawio-shapes.md`.
3. **Hand off to `@drawio/mcp`.** Call `open_drawio_xml` with the XML content. The MCP returns a draw.io URL the user can open.
4. **Confirm the result.** Summarize what's in the diagram and give the user the URL.

## AWS shape conventions

The draw.io AWS4 shape library covers all common services. Key conventions:

- Style prefix: `sketch=0;points=[];outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=#232F3E;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;html=1;fontSize=12;fontStyle=0;aspect=fixed;`
- Service shape: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<service_id>;` (e.g. `s3`, `sagemaker`, `lambda`, `iam`).
- Group container: `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;` for "AWS Cloud" boundary.
- Connector style: `endArrow=classic;html=1;rounded=0;` with edges using `source=` and `target=` references.

See `references/aws-drawio-shapes.md` for a full shape reference and a worked example matching the workshop's source/target architecture diagrams.

## Example call

After building the XML, invoke the MCP:

```text
Tool: open_drawio_xml  (from @drawio MCP)
Arguments:
  content: "<mxfile><diagram>...</diagram></mxfile>"
  lightbox: false
  dark: "auto"
```

The MCP returns a URL like `https://app.diagrams.net/#R<base64>`. Share it with the user.

## Failure modes

- **`@drawio` MCP not connected** — confirm `.kiro/settings/mcp.json` has the `drawio` entry; in Kiro CLI, run `/mcp` to check whether it loaded.
- **`npx -y @drawio/mcp@1.2.7` fails to install** — check Node.js >= 18 and network access to npm.
- **Diagram renders but shapes are missing icons** — wrong `resIcon` value; consult `references/aws-drawio-shapes.md`.

## See also

- `references/aws-drawio-shapes.md` — AWS shape library reference (workshop scope: SageMaker, S3, IAM, CloudFormation, FastAPI/EC2)
- `assets/templates/source-architecture.xml` — starter XML for "current state" diagrams
- `assets/templates/target-architecture.xml` — starter XML for "SageMaker target" diagrams
