# AWS shape reference for draw.io

draw.io ships the AWS4 shape library out of the box. Use the `mxgraph.aws4.resourceIcon` style with a `resIcon` attribute that names the specific service.

## Common service icons

| Service | `resIcon` |
|---|---|
| S3 | `mxgraph.aws4.s3` |
| Amazon SageMaker | `mxgraph.aws4.sagemaker` |
| SageMaker Studio | `mxgraph.aws4.sagemaker_studio` |
| SageMaker Processing | `mxgraph.aws4.sagemaker_train` |
| SageMaker Training | `mxgraph.aws4.sagemaker_train` |
| SageMaker Inference / Endpoint | `mxgraph.aws4.sagemaker_endpoint` |
| EC2 | `mxgraph.aws4.ec2` |
| IAM | `mxgraph.aws4.identity_and_access_management_iam` |
| IAM Role | `mxgraph.aws4.role` |
| CloudFormation | `mxgraph.aws4.cloudformation` |
| CloudWatch | `mxgraph.aws4.cloudwatch` |
| Lambda | `mxgraph.aws4.lambda` |
| ECR | `mxgraph.aws4.elastic_container_registry` |
| API Gateway | `mxgraph.aws4.api_gateway` |
| Route 53 | `mxgraph.aws4.route_53` |
| VPC | `mxgraph.aws4.vpc` |

## Cell style template

```text
sketch=0;
points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],
        [0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],
        [0,0.25,0],[0,0.5,0],[0,0.75,0],
        [1,0.25,0],[1,0.5,0],[1,0.75,0]];
outlineConnect=0;
fontColor=#232F3E;
gradientColor=none;
fillColor=#232F3E;
strokeColor=#232F3E;
dashed=0;
verticalLabelPosition=bottom;
verticalAlign=top;
align=center;
html=1;
fontSize=12;
fontStyle=0;
aspect=fixed;
shape=mxgraph.aws4.resourceIcon;
resIcon=mxgraph.aws4.s3;
```

## Group / boundary container

```text
shape=mxgraph.aws4.group;
grIcon=mxgraph.aws4.group_aws_cloud_alt;
strokeColor=#232F3E;
fillColor=none;
verticalAlign=top;
align=left;
```

## Connector

```text
endArrow=classic;
html=1;
rounded=0;
strokeColor=#232F3E;
```

## Sample structure

Top-level draw.io file:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="root" name="AWS Architecture">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- AWS Cloud boundary -->
        <mxCell id="aws_cloud" value="AWS Cloud" style="shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="900" height="600" as="geometry" />
        </mxCell>

        <!-- S3 bucket -->
        <mxCell id="s3" value="Workshop S3 bucket" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=#232F3E;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;" vertex="1" parent="aws_cloud">
          <mxGeometry x="100" y="80" width="60" height="60" as="geometry" />
        </mxCell>

        <!-- SageMaker Processing -->
        <mxCell id="sm_processing" value="SageMaker Processing" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=#232F3E;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sagemaker_train;" vertex="1" parent="aws_cloud">
          <mxGeometry x="280" y="80" width="60" height="60" as="geometry" />
        </mxCell>

        <!-- Edge: S3 -> Processing -->
        <mxCell id="e1" style="endArrow=classic;html=1;rounded=0;strokeColor=#232F3E;" edge="1" parent="aws_cloud" source="s3" target="sm_processing">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Hand the XML string to `open_drawio_xml` (the `@drawio/mcp` tool) and the editor opens with the rendered diagram.
