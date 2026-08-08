export type Client = {
  id: number
  first_name: string
  last_name: string
  phone: string
  email: string | null
  notes: string | null
  created_at: string
  updated_at: string
}

export type ClientPayload = {
  first_name: string
  last_name: string
  phone: string
  email: string | null
  notes: string | null
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  })

  if (!response.ok) {
    throw new Error("Si è verificato un errore durante la richiesta.")
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export function getClients(search = ""): Promise<Client[]> {
  const params = new URLSearchParams()

  if (search.trim()) {
    params.set("search", search.trim())
  }

  const queryString = params.size ? `?${params.toString()}` : ""

  return request<Client[]>(`/clients${queryString}`)
}

export function createClient(payload: ClientPayload): Promise<Client> {
  return request<Client>("/clients", {
    method: "POST",
    body: JSON.stringify(payload),
  })
}

export function updateClient(
  clientId: number,
  payload: ClientPayload,
): Promise<Client> {
  return request<Client>(`/clients/${clientId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  })
}

export function deleteClient(clientId: number): Promise<void> {
  return request<void>(`/clients/${clientId}`, {
    method: "DELETE",
  })
}
