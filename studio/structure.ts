import type {StructureResolver} from 'sanity/structure'

// Lists the 4 document types in taxonomy order (Category -> Subcategory ->
// Leaf -> Product) instead of the default alphabetical order, since that's
// the order you'll actually work through when entering a new product.
export const structure: StructureResolver = (S) =>
  S.list()
    .title('Kaleido Content')
    .items([
      S.documentTypeListItem('category').title('Categories'),
      S.documentTypeListItem('subcategory').title('Subcategories'),
      S.documentTypeListItem('leaf').title('Leaves (Product Types)'),
      S.documentTypeListItem('product').title('Products'),
    ])
