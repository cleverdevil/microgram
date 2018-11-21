Microgram
=========

Code used for creating a "Photo Index" page for a Micro.blog hosted website.

Currently used on [my wife's site](http://cleverangel.org/pictures).

To use, simply create a page on your Micro.blog website with the following
content:

```html
<div id="microgram">
  Loading...
</div>

<script src="https://microgram.cleverdevil.io/js?tz=US/Pacific"></script>
```

This will inject some JavaScript into the page, which will then discover and
crawl your feeds for photos and populate the content for you.

Make sure to pass the appropriate time zone. If none is specified in the request
for the JavaScript, then 'US/Pacific' will be assumed. For a full listing of
available time zone strings, refer to [the IANA time zone
database](https://www.iana.org/time-zones).

Note: this is still relatively experimental, and has some assumptions baked in
that need to be made configurable on a per-website basis.
