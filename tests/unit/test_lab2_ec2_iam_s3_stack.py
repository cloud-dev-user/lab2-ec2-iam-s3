import aws_cdk as core
import aws_cdk.assertions as assertions

from lab2_ec2_iam_s3.lab2_ec2_iam_s3_stack import Lab2Ec2IamS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in lab2_ec2_iam_s3/lab2_ec2_iam_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Lab2Ec2IamS3Stack(app, "lab2-ec2-iam-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
