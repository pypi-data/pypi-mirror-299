r'''
# Amazon Aurora Vector Store Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) TypeScript|`@cdklabs/generative-ai-cdk-constructs`|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`cdklabs.generative_ai_cdk_constructs`|

This construct library provides a class that defines a `AmazonAuroraVectorStore` class for an existing Amazon Aurora to be used for a vector store for a Knowledge Base. Additionally, it provides an `AmazonAuroraDefaultVectorStore` L3 resource that creates a VPC with 3 subnets (public private with NAT Gateway, private without NAT Gateway), with the Amazon Aurora Serverless V2 Cluster. The cluster has 1 writer/reader instance with PostgreSQL 15.5 version (min capacity 0.5, max capacity 4). Lambda custom resource executes required pgvector and Amazon Bedrock Knowledge Base SQL queries (see more [here](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)) against Aurora cluster during deployment. The secret containing databases credentials is being deployed and securely stored in AWS Secrets Manager. You must specify the same embeddings model that you are going to use in KnowledgeBase construct.

## Table of contents

* [API](#api)
* [Amazon Aurora Vector Store](#amazon-aurora-vector-store)
* [Amazon Aurora Default Vector Store](#amazon-aurora-default-vector-store)

## API

See the [API documentation](../../../apidocs/namespaces/amazonaurora/README.md).

## Amazon Aurora Vector Store

TypeScript

```python
import { amazonaurora } from '@cdklabs/generative-ai-cdk-constructs';

new amazonaurora.AmazonAuroraVectoStore(
  {
    resourceArn: 'arn:aws:rds:your-region:123456789876:cluster:aurora-cluster-manual',
    databaseName: 'bedrock_vector_db',
    tableName: 'bedrock_integration.bedrock_kb',
    credentialsSecretArn: 'arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
    primaryKeyField: 'id',
    vectorField: 'embedding',
    textField: 'chunks',
    metadataField: 'metadata',
  });
```

Python

```python

from cdklabs.generative_ai_cdk_constructs import (
    amazonaurora
)

aurora = amazonaurora.AmazonAuroraVectorStore(
            credentials_secret_arn='arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
            database_name='bedrock_vector_db',
            metadata_field='metadata',
            primary_key_field='id',
            resource_arn='arn:aws:rds:your-region:123456789876:cluster:aurora-cluster-manual',
            table_name='bedrock_integration.bedrock_kb',
            text_field='chunks',
            vector_field='embedding',
        )
```

## Amazon Aurora Default Vector Store

TypeScript

```python
import { amazonaurora } from '@cdklabs/generative-ai-cdk-constructs';

new amazonaurora.AmazonAuroraDefaultVectorStore(stack, 'AuroraDefaultVectorStore', {
  embeddingsModel: BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3.vectorDimensions!,
});
```

Python

```python
from cdklabs.generative_ai_cdk_constructs import (
    amazonaurora,
    bedrock
)

dimension = bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3.vector_dimensions

aurora = amazonaurora.AmazonAuroraDefaultVectorStore(self, 'AuroraDefaultVectorStore',
    embeddings_model_vector_dimension=dimension
)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class AmazonAuroraDefaultVectorStore(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.amazonaurora.AmazonAuroraDefaultVectorStore",
):
    '''(experimental) Creates default AmazonAuroraVectorStore.

    It includes creation of a VPC with 1 subnets (private isolated),
    with the Amazon Aurora Serverless V2 Cluster.
    The cluster has 1 writer/reader of PostgreSQL version 15.5
    instance (min capacity 0.5, max capacity 4). Lambda custom
    resource executes required pgvector and Amazon Bedrock Knowledge
    Base SQL queries against Aurora cluster
    during deployment. The secret containing databases credentials is
    being deployed and securely stored in AWS Secrets Manager.
    You must specify the same embeddings model that you used in
    KnowledgeBase construct.

    :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        embeddings_model_vector_dimension: jsii.Number,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param embeddings_model_vector_dimension: (experimental) The embeddings model vector dimension for the knowledge base. Must be identical as in the KnowledgeBase construct. This is due to the factor that the embeddings models have different vector dimensions and this construct needs to know the vector dimensions to create the vector index of appropriate dimensions in the Aurora database.
        :param vpc: (experimental) The VPC where the Aurora Vector Store will be deployed in. The provided VPC must have at least one subnet of type ``ec2.SubnetType.PRIVATE_ISOLATED``. If no subnets of these types are available, the deployment will fail. If not provided, a new VPC with the required subnet configuration will be created automatically. Default: - "A new VPC will be created."

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45480ec93a89a33c1e7441e7cf39edfea22947c8954f290dfab20488b2e22dd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AmazonAuroraDefaultVectorStoreProps(
            embeddings_model_vector_dimension=embeddings_model_vector_dimension,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="auroraSecurityGroup")
    def aurora_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''(experimental) The Security Group attached to the Aurora DB Instances in the Cluster.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "auroraSecurityGroup"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Cluster identifier of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="credentialsSecretArn")
    def credentials_secret_arn(self) -> builtins.str:
        '''(experimental) The Secret ARN of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "credentialsSecretArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''(experimental) The name of your Database.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="embeddingsModelVectorDimension")
    def embeddings_model_vector_dimension(self) -> jsii.Number:
        '''(experimental) Model used for embeddings.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "embeddingsModelVectorDimension"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyField")
    def primary_key_field(self) -> builtins.str:
        '''(experimental) Primary key of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "primaryKeyField"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''(experimental) The ARN of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The Table Name of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The VPC where the Aurora DB Cluster is deployed.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.amazonaurora.AmazonAuroraDefaultVectorStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "embeddings_model_vector_dimension": "embeddingsModelVectorDimension",
        "vpc": "vpc",
    },
)
class AmazonAuroraDefaultVectorStoreProps:
    def __init__(
        self,
        *,
        embeddings_model_vector_dimension: jsii.Number,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param embeddings_model_vector_dimension: (experimental) The embeddings model vector dimension for the knowledge base. Must be identical as in the KnowledgeBase construct. This is due to the factor that the embeddings models have different vector dimensions and this construct needs to know the vector dimensions to create the vector index of appropriate dimensions in the Aurora database.
        :param vpc: (experimental) The VPC where the Aurora Vector Store will be deployed in. The provided VPC must have at least one subnet of type ``ec2.SubnetType.PRIVATE_ISOLATED``. If no subnets of these types are available, the deployment will fail. If not provided, a new VPC with the required subnet configuration will be created automatically. Default: - "A new VPC will be created."

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d899f08c4e4913e25c1c6185fd49e7faa77d4363934070a9d84a79b9c6e7bb)
            check_type(argname="argument embeddings_model_vector_dimension", value=embeddings_model_vector_dimension, expected_type=type_hints["embeddings_model_vector_dimension"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "embeddings_model_vector_dimension": embeddings_model_vector_dimension,
        }
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def embeddings_model_vector_dimension(self) -> jsii.Number:
        '''(experimental) The embeddings model vector dimension for the knowledge base.

        Must be identical as in the KnowledgeBase construct.
        This is due to the factor that the embeddings models
        have different vector dimensions and this construct
        needs to know the vector dimensions to create the vector
        index of appropriate dimensions in the Aurora database.

        :stability: experimental
        '''
        result = self._values.get("embeddings_model_vector_dimension")
        assert result is not None, "Required property 'embeddings_model_vector_dimension' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) The VPC where the Aurora Vector Store will be deployed in.

        The provided VPC must have at least one subnet of type
        ``ec2.SubnetType.PRIVATE_ISOLATED``. If no subnets of these
        types are available, the deployment will fail.
        If not provided, a new VPC with the required subnet
        configuration will be created automatically.

        :default: - "A new VPC will be created."

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonAuroraDefaultVectorStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AmazonAuroraVectorStore(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.amazonaurora.AmazonAuroraVectorStore",
):
    '''(experimental) Class to define a AmazonAuroraVectorStore.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        credentials_secret_arn: builtins.str,
        database_name: builtins.str,
        metadata_field: builtins.str,
        primary_key_field: builtins.str,
        resource_arn: builtins.str,
        table_name: builtins.str,
        text_field: builtins.str,
        vector_field: builtins.str,
    ) -> None:
        '''
        :param credentials_secret_arn: (experimental) The Secret ARN of your Amazon Aurora DB cluster.
        :param database_name: (experimental) The name of your Database.
        :param metadata_field: (experimental) Provide the metadata field that you configured in Amazon Aurora.
        :param primary_key_field: (experimental) Provide the primary key that you configured in Amazon Aurora.
        :param resource_arn: (experimental) The ARN of your Amazon Aurora DB cluster.
        :param table_name: (experimental) The Table Name of your Amazon Aurora DB cluster.
        :param text_field: (experimental) Provide the text field that you configured in Amazon Aurora.
        :param vector_field: (experimental) Provide the vector field that you configured in Amazon Aurora.

        :stability: experimental
        '''
        props = AmazonAuroraVectorStoreProps(
            credentials_secret_arn=credentials_secret_arn,
            database_name=database_name,
            metadata_field=metadata_field,
            primary_key_field=primary_key_field,
            resource_arn=resource_arn,
            table_name=table_name,
            text_field=text_field,
            vector_field=vector_field,
        )

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="credentialsSecretArn")
    def credentials_secret_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "credentialsSecretArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="metadataField")
    def metadata_field(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "metadataField"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyField")
    def primary_key_field(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "primaryKeyField"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="textField")
    def text_field(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "textField"))

    @builtins.property
    @jsii.member(jsii_name="vectorField")
    def vector_field(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "vectorField"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.amazonaurora.AmazonAuroraVectorStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "credentials_secret_arn": "credentialsSecretArn",
        "database_name": "databaseName",
        "metadata_field": "metadataField",
        "primary_key_field": "primaryKeyField",
        "resource_arn": "resourceArn",
        "table_name": "tableName",
        "text_field": "textField",
        "vector_field": "vectorField",
    },
)
class AmazonAuroraVectorStoreProps:
    def __init__(
        self,
        *,
        credentials_secret_arn: builtins.str,
        database_name: builtins.str,
        metadata_field: builtins.str,
        primary_key_field: builtins.str,
        resource_arn: builtins.str,
        table_name: builtins.str,
        text_field: builtins.str,
        vector_field: builtins.str,
    ) -> None:
        '''(experimental) Properties for a AmazonAuroraVectorStore.

        :param credentials_secret_arn: (experimental) The Secret ARN of your Amazon Aurora DB cluster.
        :param database_name: (experimental) The name of your Database.
        :param metadata_field: (experimental) Provide the metadata field that you configured in Amazon Aurora.
        :param primary_key_field: (experimental) Provide the primary key that you configured in Amazon Aurora.
        :param resource_arn: (experimental) The ARN of your Amazon Aurora DB cluster.
        :param table_name: (experimental) The Table Name of your Amazon Aurora DB cluster.
        :param text_field: (experimental) Provide the text field that you configured in Amazon Aurora.
        :param vector_field: (experimental) Provide the vector field that you configured in Amazon Aurora.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479db2f7e67505b8a3b5fb3b16af4aa17abcf77b50dc07738fe9abab2f5fc209)
            check_type(argname="argument credentials_secret_arn", value=credentials_secret_arn, expected_type=type_hints["credentials_secret_arn"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument metadata_field", value=metadata_field, expected_type=type_hints["metadata_field"])
            check_type(argname="argument primary_key_field", value=primary_key_field, expected_type=type_hints["primary_key_field"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument text_field", value=text_field, expected_type=type_hints["text_field"])
            check_type(argname="argument vector_field", value=vector_field, expected_type=type_hints["vector_field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials_secret_arn": credentials_secret_arn,
            "database_name": database_name,
            "metadata_field": metadata_field,
            "primary_key_field": primary_key_field,
            "resource_arn": resource_arn,
            "table_name": table_name,
            "text_field": text_field,
            "vector_field": vector_field,
        }

    @builtins.property
    def credentials_secret_arn(self) -> builtins.str:
        '''(experimental) The Secret ARN of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        result = self._values.get("credentials_secret_arn")
        assert result is not None, "Required property 'credentials_secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''(experimental) The name of your Database.

        :stability: experimental
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_field(self) -> builtins.str:
        '''(experimental) Provide the metadata field that you configured in Amazon Aurora.

        :stability: experimental
        '''
        result = self._values.get("metadata_field")
        assert result is not None, "Required property 'metadata_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key_field(self) -> builtins.str:
        '''(experimental) Provide the primary key that you configured in Amazon Aurora.

        :stability: experimental
        '''
        result = self._values.get("primary_key_field")
        assert result is not None, "Required property 'primary_key_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''(experimental) The ARN of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''(experimental) The Table Name of your Amazon Aurora DB cluster.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text_field(self) -> builtins.str:
        '''(experimental) Provide the text field that you configured in Amazon Aurora.

        :stability: experimental
        '''
        result = self._values.get("text_field")
        assert result is not None, "Required property 'text_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vector_field(self) -> builtins.str:
        '''(experimental) Provide the vector field that you configured in Amazon Aurora.

        :stability: experimental
        '''
        result = self._values.get("vector_field")
        assert result is not None, "Required property 'vector_field' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmazonAuroraVectorStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmazonAuroraDefaultVectorStore",
    "AmazonAuroraDefaultVectorStoreProps",
    "AmazonAuroraVectorStore",
    "AmazonAuroraVectorStoreProps",
]

publication.publish()

def _typecheckingstub__45480ec93a89a33c1e7441e7cf39edfea22947c8954f290dfab20488b2e22dd2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    embeddings_model_vector_dimension: jsii.Number,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d899f08c4e4913e25c1c6185fd49e7faa77d4363934070a9d84a79b9c6e7bb(
    *,
    embeddings_model_vector_dimension: jsii.Number,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479db2f7e67505b8a3b5fb3b16af4aa17abcf77b50dc07738fe9abab2f5fc209(
    *,
    credentials_secret_arn: builtins.str,
    database_name: builtins.str,
    metadata_field: builtins.str,
    primary_key_field: builtins.str,
    resource_arn: builtins.str,
    table_name: builtins.str,
    text_field: builtins.str,
    vector_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
