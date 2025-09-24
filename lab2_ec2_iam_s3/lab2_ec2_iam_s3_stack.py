from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
    aws_ssm as ssm,
    RemovalPolicy
)
from constructs import Construct

class Lab2Ec2IamS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ---- Fetch parameters from SSM ----
        instance_type = ssm.StringParameter.from_string_parameter_name(
            self, "InstanceTypeParam",
            string_parameter_name="/lab2/instanceType"
        ).string_value

        key_name = ssm.StringParameter.from_string_parameter_name(
            self, "KeyNameParam",
            string_parameter_name="/lab2/keyName"
        ).string_value

        bucket_name = ssm.StringParameter.from_string_parameter_name(
            self, "BucketNameParam",
            string_parameter_name="/lab2/bucketName"
        ).string_value

        vpc_id = ssm.StringParameter.from_string_parameter_name(
            self, "VpcIdParam",
            string_parameter_name="/lab2/vpcId"
        ).string_value

        # ---- IAM Role for EC2 ----
        role = iam.Role(self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )
        
        # ---- Use existing VPC from SSM ----
        vpc = ec2.Vpc.from_lookup(self, "ExistingVPC",
            vpc_id=vpc_id
        )
        # ---- Security Group ----
        sg = ec2.SecurityGroup(self, "EC2SG",
            vpc=vpc,
            description="Allow SSH",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")

        # ---- EC2 Instance ----
        ec2_instance = ec2.Instance(self, "MyInstance",
            vpc=vpc,
            instance_type=ec2.InstanceType(instance_type),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            key_name=key_name,
            role=role,
            security_group=sg
        )

        # ---- S3 Bucket ----
        bucket = s3.Bucket(self, "MyBucket",
            bucket_name=bucket_name,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

