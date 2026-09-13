import {defineField, defineType, defineArrayMember} from 'sanity'
import {DocumentTextIcon} from '@sanity/icons/DocumentText'
import {slugify} from './lib/slugify'

// Body uses standard Portable Text so posts can have real rich formatting in
// Studio (headings, bold, bullet lists). generate_blog.py renders it to HTML
// itself (no JS/Node in that pipeline) and uses the h2-style blocks to build
// the same numbered table-of-contents the placeholder posts already have.
export const post = defineType({
  name: 'post',
  title: 'Blog Post',
  type: 'document',
  icon: DocumentTextIcon,
  groups: [
    {name: 'content', title: 'Content', default: true},
    {name: 'meta', title: 'Meta'},
  ],
  fields: [
    defineField({
      name: 'title',
      title: 'Title',
      type: 'string',
      group: 'content',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      description: 'Used in the URL: /blog/<slug>/.',
      group: 'content',
      options: {source: 'title', slugify, maxLength: 96},
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'excerpt',
      title: 'Excerpt',
      type: 'text',
      rows: 3,
      description: 'Shown on blog cards and in the page <meta description>.',
      group: 'content',
      validation: (rule) => rule.required().max(240),
    }),
    defineField({
      name: 'tldr',
      title: 'TL;DR',
      type: 'text',
      rows: 3,
      description: 'Shown in the collapsible "Click for the TL;DR" box at the top of the post.',
      group: 'content',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'coverImage',
      title: 'Cover Image',
      type: 'image',
      options: {hotspot: true},
      group: 'content',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'body',
      title: 'Body',
      type: 'array',
      group: 'content',
      description:
        'Use Heading 2 to start a new section — each one becomes an entry in the table of contents automatically.',
      of: [
        defineArrayMember({
          type: 'block',
          styles: [
            {title: 'Normal', value: 'normal'},
            {title: 'Heading 2', value: 'h2'},
          ],
          lists: [{title: 'Bullet', value: 'bullet'}],
          marks: {
            decorators: [
              {title: 'Bold', value: 'strong'},
              {title: 'Italic', value: 'em'},
            ],
          },
        }),
      ],
      validation: (rule) => rule.required().min(1),
    }),
    defineField({
      name: 'category',
      title: 'Category',
      type: 'string',
      description: 'A short tag, e.g. "Sourcing", "Procurement" — used for the filter chips on /blog.html.',
      group: 'meta',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'author',
      title: 'Author',
      type: 'string',
      group: 'meta',
      initialValue: 'Kaleido Team',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'readMinutes',
      title: 'Read Time (minutes)',
      type: 'number',
      group: 'meta',
      validation: (rule) => rule.required().positive().integer(),
    }),
    defineField({
      name: 'publishedDate',
      title: 'Published Date',
      type: 'date',
      group: 'meta',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'featured',
      title: 'Featured?',
      type: 'boolean',
      description: 'The featured post is shown in the banner at the top of /blog.html. Only mark one post featured at a time.',
      group: 'meta',
      initialValue: false,
    }),
  ],
  preview: {
    select: {title: 'title', subtitle: 'category', media: 'coverImage', featured: 'featured'},
    prepare: ({title, subtitle, media, featured}) => ({
      title: featured ? `★ ${title}` : title,
      subtitle,
      media,
    }),
  },
  orderings: [
    {
      title: 'Published Date, New First',
      name: 'publishedDateDesc',
      by: [{field: 'publishedDate', direction: 'desc'}],
    },
  ],
})
