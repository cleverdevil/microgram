Microgram
=========

Code used for creating a "Photo Index" page for a Micro.blog hosted website.

Currently used on [my wife's site](http://cleverangel.org/pictures).

To use, simply create a page on your Micro.blog website with the following
content:

```html
<link type="text/css" rel="stylesheet" href="https://microgram.cleverdevil.io/css" />

<div id="microgram">
  Loading ...
</div>

<script src="https://microgram.cleverdevil.io/js"></script>
```

This will inject some JavaScript into the page, which will then discover and
crawl your feeds for photos and populate the content for you.

Note: this is still relatively experimental, and has some assumptions baked in
that need to be made configurable on a per-website basis.
