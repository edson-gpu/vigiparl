import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VigiParl — La transparence parlementaire pour tous",
  description:
    "Consultez chaque vote de l'Assemblée nationale, résumé par IA en 5 lignes, mis à jour en temps réel.",
  keywords: ["parlement", "votes", "députés", "transparence", "assemblée nationale"],
  openGraph: {
    title: "VigiParl",
    description: "La transparence parlementaire pour tous",
    url: "https://vigiparl.fr",
    siteName: "VigiParl",
    locale: "fr_FR",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-gray-50 font-sans antialiased">
        <header className="bg-navy text-white shadow-md">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              <a href="/" className="flex items-center gap-2">
                <span className="text-2xl font-bold tracking-tight">VigiParl</span>
                <span className="hidden text-sm text-navy-100 sm:block">
                  La transparence parlementaire pour tous
                </span>
              </a>
              <nav className="flex gap-6 text-sm font-medium">
                <a href="/votes" className="hover:text-civic transition-colors">Votes</a>
                <a href="/deputes" className="hover:text-civic transition-colors">Députés</a>
                <a href="/compare" className="hover:text-civic transition-colors">Comparateur</a>
                <a href="/recherche" className="hover:text-civic transition-colors">Recherche</a>
              </nav>
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
        <footer className="mt-16 border-t bg-white py-8 text-center text-sm text-gray-500">
          <p>
            VigiParl — Données officielles Assemblée Nationale &amp; Légifrance |{" "}
            <a href="https://github.com/edson-gpu/vigiparl" className="underline hover:text-navy">
              Code source open source
            </a>{" "}
            | Licence GNU AGPL v3
          </p>
          <p className="mt-1 text-xs">
            Résumés générés par IA — Texte source officiel toujours disponible
          </p>
        </footer>
      </body>
    </html>
  );
}
