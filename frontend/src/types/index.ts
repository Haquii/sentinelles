export interface Resource {
  id: number;
  resource_type: string;
  title: string;
  url?: string;
  author?: string;
  publisher?: string;
  year?: number;
  description?: string;
  is_primary: boolean;
  language: string;
}

export interface Whistleblower {
  id: number;
  name: string;
  photo_url?: string;
  nationality?: string;
  birth_year?: number;
  case_title: string;
  revelation_date?: string;
  revelation_year?: number;
  summary: string;
  context?: string;
  stakes?: string;
  impact?: string;
  status: WhistleblowerStatus;
  refuge_country?: string;
  personal_consequences?: string;
  is_protected: boolean;
  awards?: string;
  domains: string[];
  resources?: Resource[];
  is_featured: boolean;
  is_verified: boolean;
}

export type WhistleblowerStatus = 
  | 'libre'
  | 'exilé'
  | 'emprisonné'
  | 'en procès'
  | 'réhabilité'
  | 'décédé'
  | 'anonyme'
  | 'inconnu';

export interface Domain {
  domain: string;
  count: number;
}

export interface Stats {
  total_whistleblowers: number;
  by_status: Record<string, number>;
  by_domain: Record<string, number>;
  featured_count: number;
}

export const domainLabels: Record<string, string> = {
  'finance': 'Finance',
  'environnement': 'Environnement',
  'santé': 'Santé',
  'surveillance': 'Surveillance',
  'défense': 'Défense',
  'corruption': 'Corruption',
  'droits humains': 'Droits humains',
  'fiscalité': 'Fiscalité',
  'nucléaire': 'Nucléaire',
  'agroalimentaire': 'Agroalimentaire',
  'pharmaceutique': 'Pharmaceutique',
  'technologie': 'Technologie',
  'autre': 'Autre',
};

export const statusLabels: Record<string, string> = {
  'libre': 'Libre',
  'exilé': 'En exil',
  'emprisonné': 'Emprisonné',
  'en procès': 'En procès',
  'réhabilité': 'Réhabilité',
  'décédé': 'Décédé',
  'anonyme': 'Anonyme',
  'inconnu': 'Inconnu',
};

export const statusColors: Record<string, string> = {
  'libre': 'status-libre',
  'exilé': 'status-exile',
  'emprisonné': 'status-emprisonne',
  'en procès': 'status-proces',
  'réhabilité': 'status-rehabilite',
  'décédé': 'status-decede',
  'anonyme': 'status-anonyme',
  'inconnu': 'status-inconnu',
};
