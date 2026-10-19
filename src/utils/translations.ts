import { getCollection, type CollectionEntry } from 'astro:content';
import { siteConfig } from '../config/site';
import { TRANSLATED_LANGS, postPath, type Lang } from '../i18n';

export async function getTranslations(): Promise<CollectionEntry<'translations'>[]> {
	return (await getCollection('translations')).filter((entry) => !entry.data.draft);
}

export function translationSlug(entry: CollectionEntry<'translations'>): string {
	return entry.data.source;
}

export async function alternatesFor(slug: string): Promise<Array<{ lang: Lang; href: string }>> {
	const translations = await getTranslations();
	const available = new Set(translations.filter((entry) => entry.data.source === slug).map((entry) => entry.data.lang));
	const langs: Lang[] = ['en', ...TRANSLATED_LANGS.filter((lang) => available.has(lang))];
	return langs.map((lang) => ({ lang, href: `${siteConfig.site}${postPath(lang, slug)}` }));
}
