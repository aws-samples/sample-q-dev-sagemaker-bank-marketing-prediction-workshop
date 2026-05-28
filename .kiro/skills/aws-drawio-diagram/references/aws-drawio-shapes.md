# AWS4 shape reference for draw.io (verified 2025)

The `mxgraph.aws4` stencil library is built into draw.io. It contains 1032+ shapes.
This reference documents the CORRECT usage pattern that renders icons properly.

## The ONE correct style pattern

```
sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=<SERVICE_COLOR>;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<SHAPE_NAME>;
```

Replace:
- `<SERVICE_COLOR>` with the AWS category color (see table below)
- `<SHAPE_NAME>` with the exact stencil name (see catalog below)

## CRITICAL: Why icons appear as blank dark squares

The `resourceIcon` shape draws a colored square (`fillColor`) with a white icon overlay.

- ✅ `fillColor=#3F8624;strokeColor=#ffffff` → green square with white S3 icon
- ❌ `fillColor=#232F3E;strokeColor=#232F3E` → dark square with invisible dark icon

**ALWAYS use the service category color for `fillColor` and `#ffffff` for `strokeColor`.**

## AWS service category colors

| Category | fillColor | Example services |
|---|---|---|
| Storage | `#3F8624` | S3, EFS, FSx, Glacier, Storage Gateway |
| Machine Learning | `#01A88D` | SageMaker, Bedrock, Comprehend, Rekognition, Lex |
| Containers | `#ED7100` | ECR, ECS, EKS, Fargate |
| Compute | `#ED7100` | EC2, Lambda, Batch, Lightsail |
| Security | `#BF0816` | IAM, Cognito, GuardDuty, WAF, Shield |
| Management & Governance | `#E7157B` | CloudWatch, CloudFormation, Config, SSM |
| Networking | `#8C4FFF` | VPC, Route 53, CloudFront, API Gateway, Direct Connect |
| Database | `#C925D1` | RDS, DynamoDB, ElastiCache, Neptune |
| Analytics | `#8C4FFF` | Athena, Redshift, EMR, Kinesis, Glue |
| Application Integration | `#E7157B` | SQS, SNS, EventBridge, Step Functions |
| Developer Tools | `#C925D1` | CodePipeline, CodeBuild, CodeDeploy |
| Migration | `#ED7100` | DMS, Migration Hub, Transfer Family |

## Verified shape names (most common)

These are confirmed to exist in the `mxgraph.aws4` catalog. Use the EXACT string after `resIcon=mxgraph.aws4.`.

### Storage
| Service | resIcon value |
|---|---|
| Amazon S3 | `s3` |
| S3 Bucket (bucket icon) | `bucket` |
| S3 Glacier | `glacier` |
| EFS | `elastic_file_system` |
| FSx | `fsx` |
| Storage Gateway | `storage_gateway` |
| Backup | `backup` |

### Machine Learning
| Service | resIcon value |
|---|---|
| SageMaker (generic) | `sagemaker` |
| SageMaker Training | `sagemaker_train` |
| SageMaker Model | `sagemaker_model` |
| SageMaker Notebook | `sagemaker_notebook` |
| SageMaker Endpoint | `endpoint` |
| SageMaker Ground Truth | `sagemaker_ground_truth` |
| Bedrock | `bedrock` |
| Comprehend | `comprehend` |
| Rekognition | `rekognition` |
| Lex | `lex` |
| Polly | `polly` |
| Textract | `textract` |
| Transcribe | `transcribe` |
| Translate | `translate` |
| Personalize | `personalize` |
| Forecast | `forecast` |
| Kendra | `kendra` |

### Compute
| Service | resIcon value |
|---|---|
| EC2 | `ec2` |
| Lambda | `lambda` |
| Batch | `batch` |
| Elastic Beanstalk | `elastic_beanstalk` |
| Lightsail | `lightsail` |
| Outposts | `outposts` |
| Fargate | `fargate` |

### Containers
| Service | resIcon value |
|---|---|
| ECR | `ecr` |
| ECS | `ecs` |
| EKS | `eks` |

### Security
| Service | resIcon value |
|---|---|
| IAM | `identity_and_access_management` |
| IAM Role | `role` |
| Cognito | `cognito` |
| GuardDuty | `guardduty` |
| WAF | `waf` |
| Shield | `shield` |
| Secrets Manager | `secrets_manager` |
| KMS | `key_management_service` |
| Inspector | `inspector` |
| Security Hub | `security_hub` |
| Macie | `macie` |

### Management & Governance
| Service | resIcon value |
|---|---|
| CloudWatch | `cloudwatch_2` |
| CloudFormation | `cloudformation` |
| Config | `config` |
| Systems Manager | `systems_manager` |
| CloudTrail | `cloudtrail` |
| Organizations | `organizations` |
| Trusted Advisor | `trusted_advisor` |
| Control Tower | `control_tower` |

### Networking
| Service | resIcon value |
|---|---|
| VPC | `vpc` |
| Route 53 | `route_53` |
| CloudFront | `cloudfront` |
| API Gateway | `api_gateway` |
| Direct Connect | `direct_connect` |
| Global Accelerator | `global_accelerator` |
| Elastic Load Balancing | `elastic_load_balancing` |
| Transit Gateway | `transit_gateway` |

### Database
| Service | resIcon value |
|---|---|
| RDS | `rds` |
| DynamoDB | `dynamodb` |
| ElastiCache | `elasticache` |
| Neptune | `neptune` |
| Redshift | `redshift` |
| DocumentDB | `documentdb_with_mongodb_compatibility` |
| Keyspaces | `keyspaces` |
| Timestream | `timestream` |
| MemoryDB | `memorydb_for_redis` |

### Analytics
| Service | resIcon value |
|---|---|
| Athena | `athena` |
| EMR | `emr` |
| Kinesis | `kinesis` |
| Glue | `glue` |
| Lake Formation | `lake_formation` |
| OpenSearch | `elasticsearch_service` |
| MSK | `managed_streaming_for_kafka` |
| QuickSight | `quicksight` |
| Data Exchange | `data_exchange` |

### Application Integration
| Service | resIcon value |
|---|---|
| SQS | `sqs` |
| SNS | `sns` |
| EventBridge | `eventbridge` |
| Step Functions | `step_functions` |
| AppSync | `appsync` |
| MQ | `mq` |

### Developer Tools
| Service | resIcon value |
|---|---|
| CodePipeline | `codepipeline` |
| CodeBuild | `codebuild` |
| CodeDeploy | `codedeploy` |
| CodeCommit | `codecommit` |
| Cloud9 | `cloud9` |

## Common WRONG names (do NOT use)

| Wrong | Correct |
|---|---|
| `identity_and_access_management_iam` | `identity_and_access_management` |
| `cloudwatch` (alone) | `cloudwatch_2` |
| `elastic_container_registry` | `ecr` |
| `sagemaker_endpoint` | `endpoint` |
| `sagemaker_2` | `sagemaker` (use generic) |

## Group / boundary container

```xml
<mxCell id="cloud" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;dashed=0;container=1;pointerEvents=0;collapsible=0;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="900" height="600" as="geometry" />
</mxCell>
```

## Edge / connector styles

Primary data flow (solid, colored by source service):
```
edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeColor=#3F8624;fontStyle=1;fontSize=10;
```

Secondary / infrastructure flow (dashed, gray):
```
edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;dashed=1;strokeColor=#999999;fontSize=10;
```

## File output convention

Save all diagrams to `diagrams/` directory:
```
diagrams/<descriptive-name>.drawio
```

Then call `open_drawio_xml` with the same XML to open in browser.

## Known limitation: MCP URL rendering

When `open_drawio_xml` opens a diagram via the `#create=` URL parameter, draw.io's web editor may not pre-load the AWS4 stencil library, causing icons to appear as blank colored squares. The `.drawio` file opened directly (double-click or File → Open) always renders correctly.

**Mitigation:** Always save the `.drawio` file first. The MCP open is a convenience for quick preview; the file is the reliable artifact.
