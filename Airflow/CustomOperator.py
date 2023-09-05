from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CustomOperator(BaseOperator):  
    @apply_defaults
    def __init__(self, template_field_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_field_name = template_field_name
    
    def execute(self, context):
        pass


# use CustomOperator
from airflow import DAG
with DAG(
    dag_id='test_dag', 
    default_args=default_args, 
    schedule_interval=None
) as dag:
  
    custom_task = CustomOperator(
        task_id='my_custom_task',
        template_field_name="{{ ds }}", 
    )






      
      
        
