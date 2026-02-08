"""Salesforce to BigQuery Pipeline.

This pipeline extracts CRM data from Salesforce and loads it into Google BigQuery.
"""

import dlt


@dlt.source
def salesforce_source(
    username: str = dlt.secrets.value,
    password: str = dlt.secrets.value,
    security_token: str = dlt.secrets.value,
):
    """Load Salesforce objects."""
    from simple_salesforce import Salesforce

    sf = Salesforce(username=username, password=password, security_token=security_token)

    @dlt.resource(write_disposition="merge", primary_key="Id")
    def accounts():
        """Extract Salesforce Accounts."""
        query = """
            SELECT Id, Name, Type, Industry, AnnualRevenue,
                   NumberOfEmployees, CreatedDate, LastModifiedDate
            FROM Account
            WHERE IsDeleted = false
        """
        results = sf.query_all(query)
        yield results["records"]

    @dlt.resource(write_disposition="merge", primary_key="Id")
    def opportunities():
        """Extract Salesforce Opportunities."""
        query = """
            SELECT Id, Name, AccountId, Amount, StageName,
                   Probability, CloseDate, CreatedDate, LastModifiedDate
            FROM Opportunity
            WHERE IsDeleted = false
        """
        results = sf.query_all(query)
        yield results["records"]

    @dlt.resource(write_disposition="merge", primary_key="Id")
    def contacts():
        """Extract Salesforce Contacts."""
        query = """
            SELECT Id, FirstName, LastName, Email, AccountId,
                   Title, Department, CreatedDate, LastModifiedDate
            FROM Contact
            WHERE IsDeleted = false
        """
        results = sf.query_all(query)
        yield results["records"]

    @dlt.resource(write_disposition="merge", primary_key="Id")
    def leads():
        """Extract Salesforce Leads."""
        query = """
            SELECT Id, FirstName, LastName, Company, Email,
                   Status, LeadSource, CreatedDate, LastModifiedDate
            FROM Lead
            WHERE IsDeleted = false
        """
        results = sf.query_all(query)
        yield results["records"]

    return accounts, opportunities, contacts, leads


def run():
    """Execute the Salesforce to BigQuery pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="salesforce_crm",
        destination="bigquery",
        dataset_name="salesforce_data",
    )

    # Run the pipeline
    load_info = pipeline.run(salesforce_source())

    print(f"Pipeline completed: {load_info}")
    return load_info


if __name__ == "__main__":
    run()
