import { personSameAs, siteConfig } from '../config/site';

const WEBSITE_ID = `${siteConfig.site}/#website`;
const BLOG_ID = `${siteConfig.site}/blog/#blog`;

export function buildPersonJsonLd() {
	const { author } = siteConfig;
	return {
		"@context": "https://schema.org",
		"@type": "Person",
		"@id": author.id,
		name: author.name,
		alternateName: author.alternateName,
		url: author.url,
		image: author.image,
		email: `mailto:${author.email}`,
		jobTitle: author.jobTitle,
		description: author.bio,
		knowsAbout: author.knowsAbout,
		workLocation: {
			"@type": "Place",
			name: author.location,
		},
		sameAs: personSameAs,
	};
}

export function buildWebSiteJsonLd(siteUrl: string, name: string, description: string) {
	return {
		"@context": "https://schema.org",
		"@type": "WebSite",
		"@id": WEBSITE_ID,
		name,
		alternateName: 'opendoors.wtf',
		description,
		url: `${siteUrl}/`,
		inLanguage: siteConfig.language,
		author: { "@id": siteConfig.author.id },
		publisher: { "@id": siteConfig.author.id },
	};
}

export function buildBlogJsonLd(posts: Array<{ title: string; url: string; datePublished: string }>) {
	return {
		"@context": "https://schema.org",
		"@type": "Blog",
		"@id": BLOG_ID,
		name: siteConfig.title,
		description: siteConfig.description,
		url: `${siteConfig.site}/blog/`,
		inLanguage: siteConfig.language,
		isPartOf: { "@id": WEBSITE_ID },
		author: { "@id": siteConfig.author.id },
		blogPost: posts.map((post) => ({
			"@type": "BlogPosting",
			headline: post.title,
			url: post.url,
			datePublished: post.datePublished,
		})),
	};
}

export function buildProfilePageJsonLd(url: string) {
	return {
		"@context": "https://schema.org",
		"@type": "ProfilePage",
		url,
		inLanguage: siteConfig.language,
		isPartOf: { "@id": WEBSITE_ID },
		mainEntity: { "@id": siteConfig.author.id },
	};
}

export function buildBreadcrumbJsonLd(items: Array<{ name: string; url: string }>) {
	return {
		"@context": "https://schema.org",
		"@type": "BreadcrumbList",
		itemListElement: items.map((item, index) => ({
			"@type": "ListItem",
			position: index + 1,
			name: item.name,
			item: item.url,
		})),
	};
}

export function buildBlogPostingJsonLd(params: {
	title: string;
	description: string;
	url: string;
	image: string;
	datePublished: string;
	dateModified?: string;
	keywords?: string[];
	wordCount?: number;
	markdownUrl?: string;
}) {
	return {
		"@context": "https://schema.org",
		"@type": "BlogPosting",
		"@id": `${params.url}#article`,
		headline: params.title,
		description: params.description,
		url: params.url,
		datePublished: params.datePublished,
		dateModified: params.dateModified ?? params.datePublished,
		inLanguage: siteConfig.language,
		author: {
			"@type": "Person",
			"@id": siteConfig.author.id,
			name: siteConfig.author.name,
			url: siteConfig.author.url,
			sameAs: personSameAs,
		},
		publisher: { "@id": siteConfig.author.id },
		isPartOf: { "@id": BLOG_ID },
		mainEntityOfPage: {
			"@type": "WebPage",
			"@id": params.url,
		},
		image: [params.image],
		keywords: params.keywords,
		articleSection: params.keywords?.[0],
		wordCount: params.wordCount,
		encoding: params.markdownUrl
			? { "@type": "MediaObject", encodingFormat: "text/markdown", contentUrl: params.markdownUrl }
			: undefined,
	};
}
