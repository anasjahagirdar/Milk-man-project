Place custom product images in this folder.

Recommended formats:
- `.jpg`
- `.jpeg`
- `.png`
- `.webp`
- `.avif`
- `.svg`

Examples:
- `milk.jpg`
- `curd.jpg`
- `paneer.jpg`
- `ghee.jpg`
- `butter.jpg`

How to use them:
1. Add the image file here.
2. If your backend returns an image field such as `image`, `image_url`, or `imageUrl`, that value will be used automatically.
3. If the backend does not return an image, update the `PRODUCT_IMAGE_MAP` in `customer-site/app.js` with the correct product name mapping.
4. The customer site will look for local files in this order: `.jpg`, `.jpeg`, `.png`, `.webp`, `.avif`, `.svg`.
5. If a backend image path is invalid, the customer site will fall back to the mapped local image and then to `default-dairy`.

Example:
```js
{ match: ["milk"], file: "milk" }
```
