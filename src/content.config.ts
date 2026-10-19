import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postSchema = ({ image }: { image: () => z.ZodTypeAny }) =>
	z.object({
		title: z.string(),
		description: z.string(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		draft: z.boolean().default(false),
		canonical: z.string().url().optional(),
		tags: z.array(z.string()).default([]),
		heroImage: image().optional(),
		youtube: z.string().url().optional(),
	});

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const translations = defineCollection({
	loader: glob({ base: './src/content/blog-i18n', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		postSchema({ image }).extend({
			lang: z.enum(['es', 'pt', 'de', 'fr', 'ja']),
			source: z.string(),
		}),
});

export const collections = { blog, translations };
