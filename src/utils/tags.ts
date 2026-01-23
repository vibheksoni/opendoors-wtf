export function toSlug(tag: string): string {
	return tag.trim().toLowerCase().replace(/\s+/g, '-');
}

export function toTitle(tag: string): string {
	return tag
		.trim()
		.split(/\s+/g)
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ');
}
