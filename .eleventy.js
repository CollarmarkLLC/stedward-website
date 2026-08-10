module.exports = function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy({ "src/assets/js": "assets/js" });

  // Date formatting filter
  eleventyConfig.addFilter("readableDate", (dateObj) => {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric"
    }).format(dateObj);
  });

  // Return an optimized card image only for variants generated in this repo.
  eleventyConfig.addFilter("bulletinCardImage", (imagePath) => {
    const optimizedColors = new Set(["white", "green", "purple", "red", "rose"]);
    const match = imagePath && imagePath.match(/\/([^/]+)\.jpg$/);
    return match && optimizedColors.has(match[1])
      ? imagePath.replace(/\.jpg$/, "-card.webp")
      : null;
  });

  // Sort posts by date descending
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/*.md").sort((a, b) => {
      return b.date - a.date;
    });
  });

  // The home page shows the six newest issues; the archive begins after them.
  eleventyConfig.addCollection("recentBulletins", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/*.md").sort((a, b) => {
      return b.date - a.date;
    }).slice(0, 6);
  });

  eleventyConfig.addCollection("pastBulletins", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/*.md").sort((a, b) => {
      return b.date - a.date;
    }).slice(6);
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk"
  };
};
