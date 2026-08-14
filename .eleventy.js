const { feedPlugin } = require("@11ty/eleventy-plugin-rss");

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

  // The RSS plugin reverses its source collection before rendering.
  eleventyConfig.addCollection("feedPosts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/*.md").sort((a, b) => {
      return a.date - b.date;
    });
  });

  eleventyConfig.addPlugin(feedPlugin, {
    type: "atom",
    outputPath: "/feed.xml",
    collection: {
      name: "feedPosts",
      limit: 20
    },
    metadata: {
      language: "en",
      title: "St. Edward Parish Bulletins",
      subtitle: "Weekly bulletins from St. Edward the Confessor Catholic Church in Tallulah, Louisiana.",
      base: "https://saintedwardtallulah.church/",
      author: {
        name: "St. Edward the Confessor Catholic Church"
      }
    }
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
