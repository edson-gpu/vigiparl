export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="rounded-2xl bg-navy p-10 text-white">
        <h1 className="text-4xl font-bold leading-tight">
          Chaque vote de l&apos;Assemblée nationale,
          <br />
          <span className="text-civic">résumé par IA en 5 lignes.</span>
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-navy-100">
          VigiParl rend visible ce que le pouvoir préfère invisible — parce que la démocratie commence
          par l&apos;information.
        </p>
        <div className="mt-6 flex gap-4">
          <a
            href="/votes"
            className="rounded-lg bg-civic px-6 py-3 font-semibold transition hover:bg-civic-700"
          >
            Voir les derniers votes
          </a>
          <a
            href="/deputes"
            className="rounded-lg border border-white px-6 py-3 font-semibold transition hover:bg-white hover:text-navy"
          >
            Chercher un député
          </a>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {[
          { label: "Députés suivis", value: "577" },
          { label: "Votes enregistrés", value: "—" },
          { label: "Résumés IA générés", value: "—" },
          { label: "Mise à jour", value: "Toutes les heures" },
        ].map((stat) => (
          <div key={stat.label} className="rounded-xl border bg-white p-6 text-center shadow-sm">
            <div className="text-2xl font-bold text-navy">{stat.value}</div>
            <div className="mt-1 text-sm text-gray-500">{stat.label}</div>
          </div>
        ))}
      </section>

      {/* Derniers votes placeholder */}
      <section>
        <h2 className="mb-4 text-2xl font-bold text-navy">Derniers votes</h2>
        <div className="rounded-xl border bg-white p-8 text-center text-gray-400 shadow-sm">
          <p>Les votes seront affichés ici une fois la base de données alimentée.</p>
          <a href="/votes" className="mt-4 inline-block text-navy underline">
            Voir tous les votes →
          </a>
        </div>
      </section>
    </div>
  );
}
