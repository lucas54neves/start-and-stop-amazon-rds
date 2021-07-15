import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(rds, instancia):

    rds = boto3.client('rds')

    instancia = os.getenv('DBName')

    status = get_status(rds, instancia)

    logger.info(f"Status da instancia: {status}")

    if (status != "available"):
        logger.info("Stop cancelado devido ao status diferente de 'available'")
        return {
            'stop': False,
            'motivo': f'Status {status} diferente de available'
        }

    logger.info(f"Iniciando stop RDS: {instancia}")
    response = rds.stop_db_instance(DBInstanceIdentifier=instancia)
    logger.info("Stop RDS bem sucedido: %s", response)
    return {
        'stop': True
    }


def get_status(rds, instancia):
    response = rds.describe_db_instances(DBInstanceIdentifier=instancia)
    return response['DBInstances'][0]['DBInstanceStatus']