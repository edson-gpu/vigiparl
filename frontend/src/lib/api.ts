const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  laws: {
    list: (params?: { page?: number; size?: number; statut?: string; tag?: string }) => {
      const q = new URLSearchParams(params as Record<string, string>).toString();
      return fetchAPI<{ total: number; items: Law[] }>(`/laws${q ? `?${q}` : ""}`);
    },
    get: (id: string) => fetchAPI<Law>(`/laws/${id}`),
  },
  deputies: {
    list: (params?: { page?: number; q?: string; groupe?: string }) => {
      const q = new URLSearchParams(params as Record<string, string>).toString();
      return fetchAPI<{ total: number; items: Deputy[] }>(`/deputies${q ? `?${q}` : ""}`);
    },
    get: (id: string) => fetchAPI<Deputy>(`/deputies/${id}`),
  },
};

export interface Law {
  id: string;
  an_ref: string;
  titre: string;
  type: string;
  statut: string;
  date_vote: string | null;
  resume_ai: string | null;
  impact_citoyen: string | null;
  tags: string[];
  pour_count: number;
  contre_count: number;
  abstention_count: number;
}

export interface Deputy {
  id: string;
  an_id: string;
  nom: string;
  prenom: string;
  circonscription: string | null;
  departement: string | null;
  photo_url: string | null;
  score_presence: number | null;
  score_coherence: number | null;
  parti: { sigle: string; nom: string; couleur: string | null } | null;
}
