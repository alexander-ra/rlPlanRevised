-- Two adjustments applied only when rendering a step for inclusion in a
-- bundle - never to the standalone per-step PDF.
--
-- 1. Drop a hand-written "Contents" section from a document.
--    Step 01's report carries its own Contents list in the markdown; in a
--    standalone PDF that is the author's choice, but in a bundle it
--    duplicates the merged contents and its links point inside that one
--    step. Removes the heading and everything under it up to the next
--    heading of the same or higher level.
--
-- 2. Clear title/subtitle/author/date so pandoc's default LaTeX template
--    does not emit \maketitle. A standalone PDF wants that title page; a
--    bundle already opens with one shared title page and merged contents,
--    so a second title page per chapter is a duplicate, not front matter.

-- Lua's string.lower() is ASCII-only: it leaves "Съдържание" untouched, so a
-- lowercase-only key never matched the Bulgarian heading and every BG report
-- kept its manual Contents inside the bundle. Both cases are listed instead of
-- relying on case folding.
local TITLES = {
  ["table of contents"] = true,
  ["contents"] = true,
  ["съдържание"] = true,
  ["Съдържание"] = true,
}

function Pandoc(doc)
  local out = {}
  local dropping_at = nil

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      local text = pandoc.utils.stringify(block):lower():gsub("^%s+", ""):gsub("%s+$", "")
      if dropping_at and block.level <= dropping_at then
        dropping_at = nil          -- section ended; keep this heading
      end
      if not dropping_at and TITLES[text] then
        dropping_at = block.level  -- start dropping, heading included
        goto continue
      end
    end

    if dropping_at == nil then
      out[#out + 1] = block
    end

    ::continue::
  end

  local meta = doc.meta
  meta.title = nil
  meta.subtitle = nil
  meta.author = nil
  meta.date = nil

  return pandoc.Pandoc(out, meta)
end
