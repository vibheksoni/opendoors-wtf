export function buildWebSiteJsonLd(siteUrl: string, name: string, description: string) {
	return {
		"@context": "https://schema.org",
		"@type": "WebSite",
		"@id": `${siteUrl}/#website`,
		name,
		description,
		url: siteUrl,
	};
}

export function buildOrganizationJsonLd(siteUrl: string, name: string, socials: string[]) {
	return {
		"@context": "https://schema.org",
		"@type": "Person",
		"@id": `${siteUrl}/#person`,
		name,
		url: siteUrl,
		sameAs: socials,
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
	siteUrl: string;
	title: string;
	description: string;
	url: string;
	image?: string;
	datePublished: string;
	dateModified?: string;
	authorName: string;
	authorUrl?: string;
	keywords?: string[];
}) {
	return {
		"@context": "https://schema.org",
		"@type": "BlogPosting",
		headline: params.title,
		description: params.description,
		datePublished: params.datePublished,
		dateModified: params.dateModified ?? params.datePublished,
		author: {
			"@type": "Person",
			name: params.authorName,
			url: params.authorUrl,
		},
		mainEntityOfPage: {
			"@type": "WebPage",
			"@id": params.url,
		},
		image: params.image ? [params.image] : undefined,
		keywords: params.keywords,
	};
}
