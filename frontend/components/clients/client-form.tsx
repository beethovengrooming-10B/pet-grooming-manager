"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import {
  createClient,
  type Client,
  type ClientPayload,
  updateClient,
} from "@/lib/api/clients"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const clientFormSchema = z.object({
  first_name: z.string().trim().min(1, "Il nome è obbligatorio.").max(100),
  last_name: z.string().trim().min(1, "Il cognome è obbligatorio.").max(100),
  phone: z.string().trim().min(1, "Il telefono è obbligatorio.").max(30),
  email: z.union([
    z.string().trim().email("Inserisci un'email valida."),
    z.literal(""),
  ]),
  notes: z.string().max(1000, "Le note non possono superare 1000 caratteri."),
})

type ClientFormValues = z.infer<typeof clientFormSchema>

type ClientFormProps = {
  client: Client | null
  onSaved: () => void
  onCancelEdit: () => void
}

function getDefaultValues(client: Client | null): ClientFormValues {
  return {
    first_name: client?.first_name ?? "",
    last_name: client?.last_name ?? "",
    phone: client?.phone ?? "",
    email: client?.email ?? "",
    notes: client?.notes ?? "",
  }
}

export function ClientForm({
  client,
  onSaved,
  onCancelEdit,
}: ClientFormProps) {
  const queryClient = useQueryClient()
  const form = useForm<ClientFormValues>({
    resolver: zodResolver(clientFormSchema),
    defaultValues: getDefaultValues(client),
  })

  useEffect(() => {
    form.reset(getDefaultValues(client))
  }, [client, form])

  const mutation = useMutation({
    mutationFn: (payload: ClientPayload) =>
      client
        ? updateClient(client.id, payload)
        : createClient(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["clients"] })
      form.reset(getDefaultValues(null))
      onSaved()
    },
  })

  function onSubmit(values: ClientFormValues) {
    mutation.mutate({
      first_name: values.first_name,
      last_name: values.last_name,
      phone: values.phone,
      email: values.email || null,
      notes: values.notes || null,
    })
  }

  const isEditing = client !== null

  return (
    <form className="grid gap-4" onSubmit={form.handleSubmit(onSubmit)}>
      <div className="grid gap-2">
        <Label htmlFor="first_name">Nome</Label>
        <Input id="first_name" {...form.register("first_name")} />
        {form.formState.errors.first_name && (
          <p className="text-sm text-red-600">
            {form.formState.errors.first_name.message}
          </p>
        )}
      </div>

      <div className="grid gap-2">
        <Label htmlFor="last_name">Cognome</Label>
        <Input id="last_name" {...form.register("last_name")} />
        {form.formState.errors.last_name && (
          <p className="text-sm text-red-600">
            {form.formState.errors.last_name.message}
          </p>
        )}
      </div>

      <div className="grid gap-2">
        <Label htmlFor="phone">Telefono</Label>
        <Input id="phone" type="tel" {...form.register("phone")} />
        {form.formState.errors.phone && (
          <p className="text-sm text-red-600">
            {form.formState.errors.phone.message}
          </p>
        )}
      </div>

      <div className="grid gap-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" {...form.register("email")} />
        {form.formState.errors.email && (
          <p className="text-sm text-red-600">
            {form.formState.errors.email.message}
          </p>
        )}
      </div>

      <div className="grid gap-2">
        <Label htmlFor="notes">Note</Label>
        <textarea
          id="notes"
          className="min-h-24 rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          {...form.register("notes")}
        />
        {form.formState.errors.notes && (
          <p className="text-sm text-red-600">
            {form.formState.errors.notes.message}
          </p>
        )}
      </div>

      {mutation.isError && (
        <p className="text-sm text-red-600">
          Impossibile salvare il cliente. Riprova.
        </p>
      )}

      <div className="flex gap-2">
        <Button disabled={mutation.isPending} type="submit">
          {mutation.isPending
            ? "Salvataggio..."
            : isEditing
              ? "Salva modifiche"
              : "Aggiungi cliente"}
        </Button>

        {isEditing && (
          <Button onClick={onCancelEdit} type="button" variant="outline">
            Annulla
          </Button>
        )}
      </div>
    </form>
  )
}