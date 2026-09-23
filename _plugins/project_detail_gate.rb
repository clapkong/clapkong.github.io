# frozen_string_literal: true

# Only projects with `has_detail: true` get a detail page. The rest stay in
# `site.projects` so their cards still render, but are not written, and their
# URL points at the index: the al_search palette links every collection doc by
# `item.url` from a gem template, so a gated doc would otherwise link to a 404.
module ClapkongSite
  class ProjectDetailGate < Jekyll::Generator
    priority :highest

    def generate(site)
      projects = site.collections["projects"] or return

      projects.docs.each do |doc|
        next if doc.data["has_detail"] == true

        doc.data["published"] = false
        doc.data["sitemap"] = false
        doc.data["permalink"] = "/projects/"
      end
    end
  end
end
