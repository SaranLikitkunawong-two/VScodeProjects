import Link from "next/link";
import Image from "next/image";
import { notFound } from "next/navigation";
import Footer from "@/components/Footer";
import { ARTICLE_DATA } from "@/lib/articles";

export function generateStaticParams() {
  return Object.keys(ARTICLE_DATA).map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = ARTICLE_DATA[slug];
  if (!article) return { title: "Article not found" };
  return {
    title: `${article.title} — Future Forward Planning`,
    description: article.intro,
  };
}

function RelatedCard({ slug }: { slug: string }) {
  const a = ARTICLE_DATA[slug];
  if (!a) return null;
  return (
    <Link href={`/news/${slug}`} className="related-card">
      <div className="related-card-img">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={a.image} alt={a.imageAlt} loading="lazy" />
      </div>
      <div className="related-card-body">
        <span className="chip chip-teal" style={{ fontSize: 11 }}>
          {a.cat}
        </span>
        <h3>{a.title}</h3>
        <span className="related-card-meta">
          {a.date} · {a.read}
        </span>
      </div>
    </Link>
  );
}

function Breadcrumbs({ title }: { title: string }) {
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      <Link href="/" className="breadcrumb-link">
        Home
      </Link>
      <span className="breadcrumb-sep" aria-hidden>
        /
      </span>
      <Link href="/news" className="breadcrumb-link">
        News
      </Link>
      <span className="breadcrumb-sep" aria-hidden>
        /
      </span>
      <span className="breadcrumb-current" aria-current="page">
        {title}
      </span>
    </nav>
  );
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = ARTICLE_DATA[slug];
  if (!article) notFound();

  return (
    <main id="main">
      <div className="breadcrumb-bar">
        <div className="container">
          <Breadcrumbs title={article.title} />
        </div>
      </div>

      <div className="article-hero">
        <Image src={article.image} alt={article.imageAlt} fill className="article-hero-img" sizes="100vw" priority />
        <div className="article-hero-overlay">
          <div className="container">
            <span className="chip chip-teal">{article.cat}</span>
            <h1 className="article-hero-title">{article.title}</h1>
            <div className="article-hero-meta">
              <span>{article.date}</span>
              <span className="dot" aria-hidden></span>
              <span>{article.read}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="article-body-wrap">
          <p className="lede article-intro">{article.intro}</p>
          <ul className="article-points" aria-label="Key points">
            {article.points.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>

          <div className="article-back">
            <Link href="/news" className="btn btn-secondary">
              ← Back to News
            </Link>
          </div>
        </div>
      </div>

      <section className="related-section" aria-label="Related articles">
        <div className="container">
          <h2 className="related-heading">Related articles</h2>
          <div className="related-grid">
            {article.related.map((s) => (
              <RelatedCard key={s} slug={s} />
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
