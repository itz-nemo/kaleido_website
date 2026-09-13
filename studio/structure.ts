import type {StructureResolver} from 'sanity/structure'

// Lists document types in the order you'd actually work through them:
// Category -> Subcategory -> Leaf -> Product for the catalogue, then Blog
// Posts as a separate section — instead of the default alphabetical order.
export const structure: StructureResolver = (S) =>
  S.list()
    .title('Kaleido Content')
    .items([
      S.documentTypeListItem('category').title('Categories'),
      S.documentTypeListItem('subcategory').title('Subcategories'),
      S.documentTypeListItem('leaf').title('Leaves (Product Types)'),
      S.documentTypeListItem('product').title('Products'),
      S.divider(),
      S.documentTypeListItem('post').title('Blog Posts'),
    ])
