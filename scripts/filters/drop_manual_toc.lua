-- Drop a hand-written "Contents" section from a document.
--
-- Used only when rendering a step for inclusion in a bundle. Step 01's report
-- carries its own Contents list in the markdown; in a standalone PDF that is
-- the author's choice, but in a bundle it duplicates the merged contents and
-- its links point inside that one step. Removes the heading and everything
-- under it up to the next heading of the same or higher level.

local TITLES = {
  ["table of contents"] = true,
  ["contents"] = true,
  ["съдържание"] = true,
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

  return pandoc.Pandoc(out, doc.meta)
end
