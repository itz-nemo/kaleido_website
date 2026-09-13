import {defineField, defineType} from 'sanity'
import {TagIcon} from '@sanity/icons/Tag'
import {slugify} from './lib/slugify'

export const category = defineType({
  name: 'category',
  title: 'Category',
  type: 'document',
  icon: TagIcon,
  fields: [
    defineField({
      name: 'name',
      title: 'Name',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      description: 'Used in the URL: /products/<slug>/. Matches the existing site’s scheme automatically.',
      options: {source: 'name', slugify, maxLength: 96},
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'blurb',
      title: 'Blurb',
      type: 'text',
      rows: 2,
      description: 'Short description shown under the heading on the category page.',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'isSourcingCapability',
      title: 'Sourcing capability, not a fixed catalogue?',
      type: 'boolean',
      description:
        'Turn on for categories like Strategic Sourcing that are a procurement capability rather than a browsable product catalogue — changes some copy on the category page.',
      initialValue: false,
    }),
    defineField({
      name: 'heroImage',
      title: 'Hero Image',
      type: 'image',
      options: {hotspot: true},
      description: 'Shown beside the heading on the category page and on the products.html tile.',
    }),
    defineField({
      name: 'order',
      title: 'Display Order',
      type: 'number',
      description: 'Lower numbers show first in the nav, footer, and category grid.',
      validation: (rule) => rule.required().integer(),
    }),
  ],
  preview: {
    select: {title: 'name', subtitle: 'slug.current', media: 'heroImage'},
  },
  orderings: [
    {
      title: 'Display Order',
      name: 'orderAsc',
      by: [{field: 'order', direction: 'asc'}],
    },
  ],
})
