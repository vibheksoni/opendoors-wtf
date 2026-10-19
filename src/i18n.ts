export const DEFAULT_LANG = 'en';

export const LANGUAGES = {
	en: { name: 'English', locale: 'en_US', dateLocale: 'en-US' },
	es: { name: 'Español', locale: 'es_ES', dateLocale: 'es-ES' },
	pt: { name: 'Português', locale: 'pt_BR', dateLocale: 'pt-BR' },
	de: { name: 'Deutsch', locale: 'de_DE', dateLocale: 'de-DE' },
	fr: { name: 'Français', locale: 'fr_FR', dateLocale: 'fr-FR' },
	ja: { name: '日本語', locale: 'ja_JP', dateLocale: 'ja-JP' },
} as const;

export type Lang = keyof typeof LANGUAGES;
export const TRANSLATED_LANGS = ['es', 'pt', 'de', 'fr', 'ja'] as const;

const STRINGS = {
	en: {
		readIn: 'Read in',
		writtenBy: 'Written by',
		bio: 'Backend engineer in New York. I build API infrastructure and security tools, usually by taking a protocol apart first and building on what I learn.',
		readMarkdown: 'Read as Markdown',
		support: 'If this helped you, you can',
		coffee: 'buy me a coffee',
		or: 'or',
		work: 'work with me through DevHive Studios',
		updated: 'Last updated on',
		translatedFrom: '',
		posts: 'Posts',
		postsIntro: 'Security research and backend engineering writeups by Vibhek Soni.',
		email: 'Email',
	},
	es: {
		readIn: 'Leer en',
		writtenBy: 'Escrito por',
		bio: 'Ingeniero backend en Nueva York. Construyo infraestructura de APIs y herramientas de seguridad, normalmente desarmando primero un protocolo y construyendo a partir de lo que aprendo.',
		readMarkdown: 'Leer en Markdown',
		support: 'Si esto te ayudó, puedes',
		coffee: 'invitarme un café',
		or: 'o',
		work: 'trabajar conmigo a través de DevHive Studios',
		updated: 'Actualizado el',
		translatedFrom: 'Traducido del inglés. Lee el original en',
		posts: 'Artículos',
		postsIntro: 'Investigación de seguridad e ingeniería backend por Vibhek Soni, traducidas del inglés.',
		email: 'Correo',
	},
	pt: {
		readIn: 'Ler em',
		writtenBy: 'Escrito por',
		bio: 'Engenheiro de backend em Nova York. Construo infraestrutura de APIs e ferramentas de segurança, geralmente desmontando primeiro um protocolo e construindo a partir do que aprendo.',
		readMarkdown: 'Ler em Markdown',
		support: 'Se isso te ajudou, você pode',
		coffee: 'me pagar um café',
		or: 'ou',
		work: 'trabalhar comigo pela DevHive Studios',
		updated: 'Atualizado em',
		translatedFrom: 'Traduzido do inglês. Leia o original em',
		posts: 'Artigos',
		postsIntro: 'Pesquisa de segurança e engenharia de backend por Vibhek Soni, traduzidas do inglês.',
		email: 'E-mail',
	},
	de: {
		readIn: 'Lesen auf',
		writtenBy: 'Geschrieben von',
		bio: 'Backend-Entwickler in New York. Ich baue API-Infrastruktur und Sicherheitstools, meistens indem ich zuerst ein Protokoll auseinandernehme und auf dem aufbaue, was ich dabei lerne.',
		readMarkdown: 'Als Markdown lesen',
		support: 'Wenn dir das geholfen hat, kannst du',
		coffee: 'mir einen Kaffee spendieren',
		or: 'oder',
		work: 'über DevHive Studios mit mir arbeiten',
		updated: 'Aktualisiert am',
		translatedFrom: 'Aus dem Englischen übersetzt. Original lesen auf',
		posts: 'Beiträge',
		postsIntro: 'Sicherheitsforschung und Backend-Engineering von Vibhek Soni, aus dem Englischen übersetzt.',
		email: 'E-Mail',
	},
	fr: {
		readIn: 'Lire en',
		writtenBy: 'Écrit par',
		bio: 'Ingénieur backend à New York. Je construis de l’infrastructure d’API et des outils de sécurité, en général en démontant d’abord un protocole puis en m’appuyant sur ce que j’apprends.',
		readMarkdown: 'Lire en Markdown',
		support: 'Si cet article vous a aidé, vous pouvez',
		coffee: 'm’offrir un café',
		or: 'ou',
		work: 'travailler avec moi via DevHive Studios',
		updated: 'Mis à jour le',
		translatedFrom: 'Traduit de l’anglais. Lire l’original en',
		posts: 'Articles',
		postsIntro: 'Recherche en sécurité et ingénierie backend par Vibhek Soni, traduits de l’anglais.',
		email: 'E-mail',
	},
	ja: {
		readIn: '言語',
		writtenBy: '著者',
		bio: 'ニューヨークのバックエンドエンジニア。まずプロトコルを分解し、そこで学んだことをもとに API インフラやセキュリティツールを作っています。',
		readMarkdown: 'Markdown で読む',
		support: '役に立ったら',
		coffee: 'コーヒーをおごる',
		or: 'または',
		work: 'DevHive Studios で一緒に仕事をする',
		updated: '更新日',
		translatedFrom: '英語からの翻訳です。原文は',
		posts: '記事',
		postsIntro: 'Vibhek Soni によるセキュリティ研究とバックエンドエンジニアリングの記事（英語からの翻訳）。',
		email: 'メール',
	},
} satisfies Record<Lang, Record<string, string>>;

export function t(lang: Lang) {
	return STRINGS[lang];
}

export function postPath(lang: Lang, slug: string) {
	return lang === DEFAULT_LANG ? `/blog/${slug}/` : `/${lang}/blog/${slug}/`;
}
