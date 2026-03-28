export interface RawTransaction {
  transaction_id: string;
  raw_descriptor: string;
  amount: number;
  state?: string;
  zip_code?: string;
}

export interface EnrichedTransaction {
  transaction_id: string;
  raw_descriptor: string;
  merchant_name?: string;
  merchant_address?: string;
  merchant_phone?: string;
  merchant_logo_url?: string;
}

export interface FieldScore {
  score: number;
  method: string;
  notes?: string;
}

export interface ValidationResult {
  transaction_id: string;
  raw_descriptor: string;
  composite_score: number;
  merchant_name_score?: FieldScore;
  merchant_address_score?: FieldScore;
  merchant_phone_score?: FieldScore;
  merchant_logo_score?: FieldScore;
  category?: string;
}

export interface BatchValidationResponse {
  total: number;
  avg_composite_score: number;
  results: ValidationResult[];
}
