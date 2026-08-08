"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { FormEvent, useState } from "react"

import { ClientForm } from "@/components/clients/client-form"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { deleteClient, getClients, type Client } from "@/lib/api/clients"

function formatDate(value: string) {
  return new Intl.DateTimeFormat("it-IT", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value))
}

export function ClientsPage() {
  const queryClient = useQueryClient()
  const [searchInput, setSearchInput] = useState("")
  const [search, setSearch] = useState("")
  const [editingClient, setEditingClient] = useState<Client | null>(null)

  const clientsQuery = useQuery({
    queryKey: ["clients", search],
    queryFn: () => getClients(search),
  })

  const deleteMutation = useMutation({
    mutationFn: deleteClient,
    onSuccess: async () => {
      setEditingClient(null)
      await queryClient.invalidateQueries({ queryKey: ["clients"] })
    },
  })

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSearch(searchInput)
  }

  function clearSearch() {
    setSearchInput("")
    setSearch("")
  }

  function handleDelete(client: Client) {
    const confirmed = window.confirm(
      `Vuoi eliminare ${client.first_name} ${client.last_name}?`,
    )

    if (confirmed) {
      deleteMutation.mutate(client.id)
    }
  }

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-4 py-10">
      <div>
        <p className="text-sm font-medium text-muted-foreground">
          Pet Grooming Manager
        </p>
        <h1 className="text-3xl font-bold tracking-tight">Clienti</h1>
        <p className="mt-2 text-muted-foreground">
          Gestisci l&apos;anagrafica dei clienti della toelettatura.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>
              {editingClient ? "Modifica cliente" : "Nuovo cliente"}
            </CardTitle>
            <CardDescription>
              {editingClient
                ? "Aggiorna i dati del cliente selezionato."
                : "Inserisci i dati del nuovo cliente."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ClientForm
              client={editingClient}
              onCancelEdit={() => setEditingClient(null)}
              onSaved={() => setEditingClient(null)}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Elenco clienti</CardTitle>
            <CardDescription>
              Cerca per nome, cognome o telefono.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <form className="flex gap-2" onSubmit={handleSearch}>
              <Input
                aria-label="Cerca clienti"
                onChange={(event) => setSearchInput(event.target.value)}
                placeholder="Cerca un cliente"
                value={searchInput}
              />
              <Button type="submit">Cerca</Button>
              <Button onClick={clearSearch} type="button" variant="outline">
                Azzera
              </Button>
            </form>

            {clientsQuery.isPending && (
              <p className="text-sm text-muted-foreground">
                Caricamento clienti...
              </p>
            )}

            {clientsQuery.isError && (
              <p className="text-sm text-red-600">
                Impossibile caricare i clienti. Verifica che il backend sia avviato.
              </p>
            )}

            {deleteMutation.isError && (
              <p className="text-sm text-red-600">
                Impossibile eliminare il cliente.
              </p>
            )}

            {clientsQuery.data && clientsQuery.data.length === 0 && (
              <p className="text-sm text-muted-foreground">
                Nessun cliente trovato.
              </p>
            )}

            {clientsQuery.data && clientsQuery.data.length > 0 && (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Cliente</TableHead>
                      <TableHead>Telefono</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Creato il</TableHead>
                      <TableHead className="text-right">Azioni</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {clientsQuery.data.map((client) => (
                      <TableRow key={client.id}>
                        <TableCell className="font-medium">
                          {client.first_name} {client.last_name}
                        </TableCell>
                        <TableCell>{client.phone}</TableCell>
                        <TableCell>{client.email ?? "—"}</TableCell>
                        <TableCell>{formatDate(client.created_at)}</TableCell>
                        <TableCell className="space-x-2 text-right">
                          <Button
                            onClick={() => setEditingClient(client)}
                            size="sm"
                            type="button"
                            variant="outline"
                          >
                            Modifica
                          </Button>
                          <Button
                            disabled={deleteMutation.isPending}
                            onClick={() => handleDelete(client)}
                            size="sm"
                            type="button"
                            variant="destructive"
                          >
                            Elimina
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  )
}