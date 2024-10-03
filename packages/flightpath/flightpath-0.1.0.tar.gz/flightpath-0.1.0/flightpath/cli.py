#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import csv
import sys
import logging
import getpass
import click
import duckdb
import os
from typing import List, Dict, Any, Optional

# Function to get tasks without pagination
def get_tasks(base_url: str, dag_name: str, auth: HTTPBasicAuth) -> List[Dict[str, Any]]:
    endpoint = f"{base_url}/api/v1/dags/{dag_name}/tasks"
    logging.info(f"Fetching tasks from: {endpoint}")
    
    # Make request for all tasks
    response = requests.get(endpoint, auth=auth)
    
    logging.debug(f"Response status code: {response.status_code}")
    logging.debug(f"Response content: {response.text}")

    if response.status_code != 200:
        logging.error(f"Error: Unable to fetch tasks for DAG {dag_name}. Status code: {response.status_code}")
        logging.error(f"Response content: {response.text}")
        sys.exit(1)

    return response.json()['tasks']

# Function to process tasks and build the dependency list
def build_dependencies(dag_name: str, tasks: List[Dict[str, Any]]) -> List[List[str]]:
    dependencies = []
    for task in tasks:
        upstream_task = task['task_id']
        for downstream_task in task['downstream_task_ids']:
            dependencies.append([dag_name, upstream_task, downstream_task])
    return dependencies

# Function to output the dependencies in CSV format
def output_dependencies(dependencies: List[List[str]], output_file: Optional[str] = None, output_format: str = 'csv') -> None:
    if output_format == 'csv':
        csv_header = ['dag_id', 'upstream_task_id', 'downstream_task_id']

        if output_file:
            logging.info(f"Writing output to file: {output_file}")
            with open(output_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csv_header)
                writer.writerows(dependencies)
        else:
            # Output to stdout
            writer = csv.writer(sys.stdout)
            writer.writerow(csv_header)
            writer.writerows(dependencies)
    elif output_format == 'duckdb':
        output_dependencies_to_duckdb(dependencies, output_file)
    else:
        logging.error(f"Unsupported output format: {output_format}")
        sys.exit(1)

# New function to extract dependencies
def extract_dependencies(base_url: str, dag_name: str, auth: HTTPBasicAuth, output_file: Optional[str] = None, output_format: str = 'csv') -> None:
    # Fetch tasks for the specified DAG
    logging.info(f"Starting to fetch tasks for DAG: {dag_name} from base URL: {base_url}")
    tasks = get_tasks(base_url, dag_name, auth)

    # Build dependencies from tasks
    dependencies = build_dependencies(dag_name, tasks)

    # Output dependencies to file or stdout
    output_dependencies(dependencies, output_file, output_format)
    logging.info(f"Finished processing DAG: {dag_name}")

# New function to get task instances
def get_task_instances(base_url: str, dag_id: str, dag_run_id: str, auth: HTTPBasicAuth, page_length: int = 100) -> List[Dict[str, Any]]:
    endpoint = f"{base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
    logging.info(f"Fetching task instances from: {endpoint}")
    
    all_task_instances = []
    offset = 0
    
    while True:
        params = {
            'limit': page_length,
            'offset': offset
        }
        response = requests.get(endpoint, auth=auth, params=params)
        
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.text}")

        if response.status_code != 200: 
            logging.error(f"Error: Unable to fetch task instances. Status code: {response.status_code}")
            logging.error(f"Response content: {response.text}")
            sys.exit(1)

        data = response.json()
        task_instances = data['task_instances']
        all_task_instances.extend(task_instances)
        
        if len(task_instances) < page_length:
            break
        
        offset += page_length
        logging.info(f"Fetched {len(all_task_instances)} task instances so far. Continuing to next page...")

    logging.info(f"Finished fetching all task instances. Total: {len(all_task_instances)}")
    return all_task_instances

# Function to output task instances in CSV format
def output_task_instances(task_instances: List[Dict[str, Any]], output_file: Optional[str] = None, output_format: str = 'csv') -> None:
    if output_format == 'csv':
        csv_header = [
            'task_id', 'task_display_name', 'dag_id', 'dag_run_id', 'execution_date',
            'start_date', 'end_date', 'duration', 'state', 'try_number', 'map_index',
            'max_tries', 'hostname', 'unixname', 'pool', 'pool_slots', 'queue',
            'priority_weight', 'operator', 'queued_when', 'pid', 'executor',
            'executor_config', 'rendered_map_index', 'rendered_fields', 'note'
        ]

        if output_file:
            logging.info(f"Writing output to file: {output_file}")
            with open(output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=csv_header, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(task_instances)
        else:
            # Output to stdout
            writer = csv.DictWriter(sys.stdout, fieldnames=csv_header, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(task_instances)
    elif output_format == 'duckdb':
        output_task_instances_to_duckdb(task_instances, output_file)
    else:
        logging.error(f"Unsupported output format: {output_format}")
        sys.exit(1)

# New function to extract task instances
def extract_task_instances(base_url: str, dag_id: str, dag_run_id: str, auth: HTTPBasicAuth, output_file: Optional[str] = None, output_format: str = 'csv') -> None:
    logging.info(f"Starting to fetch task instances for DAG: {dag_id}, DAG Run: {dag_run_id} from base URL: {base_url}")
    task_instances = get_task_instances(base_url, dag_id, dag_run_id, auth)
    output_task_instances(task_instances, output_file, output_format)
    logging.info(f"Finished processing task instances for DAG: {dag_id}, DAG Run: {dag_run_id}")

# New function to output dependencies to DuckDB
def output_dependencies_to_duckdb(dependencies: List[List[str]], db_path: str) -> None:
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dependencies (
            dag_id VARCHAR,
            upstream_task_id VARCHAR,
            downstream_task_id VARCHAR
        )
    """)
    conn.executemany("""
        INSERT INTO dependencies (dag_id, upstream_task_id, downstream_task_id)
        VALUES (?, ?, ?)
    """, dependencies)
    conn.close()
    logging.info(f"Dependencies written to DuckDB at {db_path}")

# New function to output task instances to DuckDB
def output_task_instances_to_duckdb(task_instances: List[Dict[str, Any]], db_path: str) -> None:
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_instances (
            task_id VARCHAR,
            task_display_name VARCHAR,
            dag_id VARCHAR,
            dag_run_id VARCHAR,
            execution_date TIMESTAMP,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            duration FLOAT,
            state VARCHAR,
            try_number INTEGER,
            map_index INTEGER,
            max_tries INTEGER,
            hostname VARCHAR,
            unixname VARCHAR,
            pool VARCHAR,
            pool_slots INTEGER,
            queue VARCHAR,
            priority_weight INTEGER,
            operator VARCHAR,
            queued_when TIMESTAMP,
            pid INTEGER,
            executor VARCHAR,
            executor_config VARCHAR,
            rendered_fields VARCHAR,
            note VARCHAR
        )
    """)
    
    # Prepare the data, ensuring we only use the columns we defined
    columns = ['task_id', 'task_display_name', 'dag_id', 'dag_run_id', 'execution_date',
               'start_date', 'end_date', 'duration', 'state', 'try_number', 'map_index',
               'max_tries', 'hostname', 'unixname', 'pool', 'pool_slots', 'queue',
               'priority_weight', 'operator', 'queued_when', 'pid', 'executor',
               'executor_config', 'rendered_fields', 'note']
    
    prepared_data = [[ti.get(col) for col in columns] for ti in task_instances]
    
    conn.executemany(f"""
        INSERT INTO task_instances ({','.join(columns)})
        VALUES ({','.join(['?' for _ in columns])})
    """, prepared_data)
    
    conn.close()
    logging.info(f"Task instances written to DuckDB at {db_path}")

# Updated main function using click with subcommands
@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Extract information from an Airflow instance."""
    # Configure logging level based on verbose flag
    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    ctx.obj = {}

@cli.command()
@click.option('-u', '--username', type=str, help='Airflow username')
@click.option('-p', '--password', type=str, help='Airflow password')
@click.option('--baseurl', required=True, help='Base URL of the Airflow instance')
@click.option('--dag-id', required=True, help='Name of the DAG')
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('--format', type=click.Choice(['csv', 'duckdb']), default='duckdb', help='Output format (duckdb or csv)')
def dependencies(username: str, password: str, baseurl: str, dag_id: str, output: Optional[str], format: str) -> None:
    """Extract DAG dependencies from an Airflow instance."""
    auth = HTTPBasicAuth(username or input("Enter Airflow username: "), 
                         password or getpass.getpass("Enter Airflow password: "))
    extract_dependencies(baseurl, dag_id, auth, output, format)

@cli.command()
@click.option('-u', '--username', type=str, help='Airflow username')
@click.option('-p', '--password', type=str, help='Airflow password')
@click.option('--baseurl', required=True, help='Base URL of the Airflow instance')
@click.option('--dag-id', required=True, help='ID of the DAG')
@click.option('--dag-run-id', required=True, help='ID of the DAG run')
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('--format', type=click.Choice(['csv', 'duckdb']), default='duckdb', help='Output format (duckdb or csv)')
def task_instances(username: str, password: str, baseurl: str, dag_id: str, dag_run_id: str, output: Optional[str], format: str) -> None:
    """Extract task instances for a specific DAG run."""
    auth = HTTPBasicAuth(username or input("Enter Airflow username: "), 
                         password or getpass.getpass("Enter Airflow password: "))
    extract_task_instances(baseurl, dag_id, dag_run_id, auth, output, format)

@cli.command()
@click.option('-u', '--username', type=str, help='Airflow username')
@click.option('-p', '--password', type=str, help='Airflow password')
@click.option('--baseurl', required=True, help='Base URL of the Airflow instance')
@click.option('--dag-id', required=True, help='ID of the DAG')
@click.option('--dag-run-id', required=True, help='ID of the DAG run')
@click.option('-o', '--output', type=click.Path(), help='Output file path prefix')
@click.option('--format', type=click.Choice(['csv', 'duckdb']), default='duckdb', help='Output format (duckdb or csv)')
@click.option('--clobber', is_flag=True, help='Delete existing output files before generating new ones')
@click.pass_context
def trace(ctx: click.Context, username: str, password: str, baseurl: str, dag_id: str, dag_run_id: str, output: Optional[str], format: str, clobber: bool) -> None:
    """Extract all data and trace a critical path."""
    auth = HTTPBasicAuth(username or input("Enter Airflow username: "), 
                         password or getpass.getpass("Enter Airflow password: "))

    if format == 'duckdb':
        dependencies_output = output
        task_instances_output = output
    elif format == 'csv':
        dependencies_output = f"{output}_dependencies.csv"
        task_instances_output = f"{output}_task_instances.csv"
    else:
        logging.error(f"Unsupported output format: {format}")
        sys.exit(1)

    if clobber:
        if format == 'duckdb':
            if os.path.exists(output):
                os.remove(output)
                logging.info(f"Deleted existing DuckDB file: {output}")
        elif format == 'csv':
            for file in [dependencies_output, task_instances_output]:
                if os.path.exists(file):
                    os.remove(file)
                    logging.info(f"Deleted existing CSV file: {file}")

    extract_dependencies(baseurl, dag_id, auth, dependencies_output, format)
    extract_task_instances(baseurl, dag_id, dag_run_id, auth, task_instances_output, format)
    
    logging.info(f"Finished extracting dependencies and task instances for DAG: {dag_id}, DAG Run: {dag_run_id}")

    # Extract and print critical path
    if format == 'duckdb':
        ctx.invoke(critical_path, dag_id=dag_id, dag_run_id=dag_run_id, duckdb_location=output)
    else:
        logging.warning("Critical path extraction is only available when using DuckDB output format.")

@cli.command()
@click.option('--dag-id', required=True, help='ID of the DAG')
@click.option('--dag-run-id', required=True, help='ID of the DAG run')
@click.option('--duckdb-location', required=True, type=click.Path(exists=True), help='Path to the DuckDB database')
def critical_path(dag_id: str, dag_run_id: str, duckdb_location: str) -> None:
    """Trace a critical path from the data previously extracted."""
    conn = duckdb.connect(duckdb_location)
    
    # Drop the critical_path table if it exists, then recreate it
    conn.execute("DROP TABLE IF EXISTS critical_path")
    conn.execute("""
    CREATE TABLE critical_path (
        dag_id VARCHAR,
        dag_run_id VARCHAR,
        task_id VARCHAR,
        unblocked_date TIMESTAMP,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        ready_seconds DECIMAL(9,2),
        running_seconds DECIMAL(9,2),
        path_index INTEGER
    )
    """)
    
    query = """
    WITH RECURSIVE critical_path_cte AS (
        SELECT 
            ti.task_id, 
            ti.start_date, 
            ti.end_date, 
            0 AS path_index
        FROM task_instances ti
        WHERE ti.end_date = (SELECT MAX(end_date) FROM task_instances WHERE dag_id = ? AND dag_run_id = ?)
        AND ti.dag_id = ? AND ti.dag_run_id = ?
        
        UNION ALL
        
        SELECT 
            ti_upstream.task_id, 
            ti_upstream.start_date, 
            ti_upstream.end_date, 
            cp.path_index + 1 AS path_index
        FROM critical_path_cte cp
        JOIN dependencies d ON d.downstream_task_id = cp.task_id
        JOIN task_instances ti_upstream ON ti_upstream.task_id = d.upstream_task_id
        WHERE ti_upstream.end_date = (
            SELECT MAX(ti_upstream2.end_date)
            FROM task_instances ti_upstream2
            JOIN dependencies d2 ON d2.upstream_task_id = ti_upstream2.task_id
            WHERE d2.downstream_task_id = cp.task_id
            AND ti_upstream2.dag_id = ? AND ti_upstream2.dag_run_id = ?
        )
        AND ti_upstream.dag_id = ? AND ti_upstream.dag_run_id = ?
    ),

    max_path_index AS (
        SELECT MAX(path_index) AS max_index FROM critical_path_cte
    )

    SELECT 
        ? AS dag_id,
        ? AS dag_run_id,
        cp.task_id,
        lead(cp.end_date) over (order by cp.path_index) as unblocked_date,
        cp.start_date, 
        cp.end_date,
        date_diff('millisecond', lead(cp.end_date) over (order by cp.path_index), cp.start_date) / 1000 as ready_seconds,
        date_diff('millisecond', cp.start_date, cp.end_date) / 1000 as running_seconds,
        mpi.max_index - cp.path_index AS path_index
    FROM critical_path_cte cp
    CROSS JOIN max_path_index mpi
    ORDER BY path_index ASC;
    """
    
    # Insert results into the critical_path table
    conn.execute(f"""
    INSERT INTO critical_path (dag_id, dag_run_id, task_id, unblocked_date, start_date, end_date, ready_seconds, running_seconds, path_index)
    {query}
    """, [dag_id, dag_run_id] * 5)
    
    # Fetch results for printing
    results = conn.execute("""
    SELECT task_id, unblocked_date, start_date, end_date, ready_seconds, running_seconds, path_index
    FROM critical_path
    WHERE dag_id = ? AND dag_run_id = ?
    ORDER BY path_index ASC
    """, [dag_id, dag_run_id]).fetchall()
    
    conn.close()
    
    # Prepare data for printing
    headers = ["Task ID", "Unblocked Date", "Start Date", "End Date", "Ready (Seconds)", "Running (Seconds)", "Path Index"]
    data = [[str(item) for item in row] for row in results]
    all_rows = [headers] + data

    # Calculate column widths
    col_widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]
    
    # Create format string
    format_string = " | ".join("{:<" + str(width) + "}" for width in col_widths)
    
    # Print results
    click.echo(format_string.format(*headers))
    click.echo("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    for row in data:
        click.echo(format_string.format(*row))

if __name__ == "__main__":
    cli()

    # poetry run flightpath trace -u admin -p admin --baseurl http://localhost:8080 --dag-id diamond_example --dag-run-id manual__2024-10-02T03:31:12.925867+00:00 --output ~/Downloads/flightpath.db --clobber