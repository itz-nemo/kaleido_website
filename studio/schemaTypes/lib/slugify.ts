// Mirrors slugify() in scripts/generate_products.py exactly, so slugs entered
// here line up with the URL scheme the static site already uses:
// lowercase, "&" -> "and", any other run of non-alphanumeric chars -> "-".
export function slugify(input: string): string {
  return input
    .toLowerCase()
    .replace(/&/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}
