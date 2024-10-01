import pandas as pd
from classes.googlesearch import GoogleSearchAPI
from classes.proxycurl import LinkedInDataProcessor
from classes.openai import OpenAIService
from lib.functions import validate_emails

class LinkedInDataEnrichmentProcessor:
    def __init__(self, cse_id: str, google_console_api_key: str, openai_key: str, proxycurl_api_key: str):
        self.google_search_api = GoogleSearchAPI(cse_id=cse_id, google_console_api_key=google_console_api_key)
        self.open_ai_service = OpenAIService(openai_key=openai_key)
        self.linkedin_data_processor = LinkedInDataProcessor(open_ai_client=self.open_ai_service, api_key_proxycurl=proxycurl_api_key)

    def process_emails(self, df: pd.DataFrame, email_col: str) -> pd.DataFrame:
        if email_col not in df.columns:
            raise ValueError(f"DataFrame must contain an '{email_col}' column")

        df = validate_emails(df, email_col)

        def process_with_google_api(row):
            if row['is_valid_email']:
                email = row[email_col]
                linkedin_url = row.get('linkedin_url') or self.google_search_api.search_linkedin_by_email(email)
                if linkedin_url:
                    row['linkedin_url'] = linkedin_url
            return row
        df = df.apply(process_with_google_api, axis=1)
        df = self.linkedin_data_processor.process_linkedin_data(df)
        return df

    def get_limits(self):
        limit = self.linkedin_data_processor.get_proxy_curl_limit()
        print(f"Current ProxyCurl credit balance: {limit}")
        return None
    
    def get_linkedin_url_by_email(self, email: str) -> str:
        if not email or not isinstance(email, str):
            return ""
        linkedin_url = self.google_search_api.search_linkedin_by_email(email)
        return linkedin_url or ""
