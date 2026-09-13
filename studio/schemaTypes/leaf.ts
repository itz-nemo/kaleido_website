import {defineField, defineType} from 'sanity'
import {ArchiveIcon} from '@sanity/icons/Archive'
import {slugify} from './lib/slugify'

// A "leaf" is the specific item type customers browse (e.g. Pens, Notebooks) —
// the level individual products get filed under. Matches the third level of
// the site's existing products/<category>/<subcategory>/<leaf>/ URL scheme.
export const leaf = defineType({
  name: 'leaf',
  title: 'Leaf (Product Type)',
  type: 'document',
  icon: ArchiveIcon,
  fields: [
    defineField({
      name: 'name',
      title: 'Name',
      type: 'string',
      description: 'e.g. "Pens", "Notebooks", "Custom Manufacturing"',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      description: 'Used in the URL: /products/<category>/<subcategory>/<slug>/.',
      options: {source: 'name', slugify, maxLength: 96},
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'subcategory',
      title: 'Subcategory',
      type: 'reference',
      to: [{type: 'subcategory'}],
      validation: (rule) => rule.required(),
    }),
  ],
  preview: {
    select: {title: 'name', subtitle: 'subcategory.name'},
  },
})
