-- Cite a source once; refer back to it afterwards.
--
-- A markdown footnote reference `[^watkins1989]` expands to a full \footnote at
-- every use, so a work cited in three places printed its whole reference three
-- times under three different numbers. What a reader wants is the reference
-- once, and a pointer to that number everywhere else.
--
-- First occurrence  -> the footnote, plus a \label.
-- Later occurrences -> a superscript \ref to that label, so it shows the
--                      ORIGINAL number rather than minting a new one.
--
-- Footnotes are matched by their rendered text, which is what makes this safe:
-- two notes that read identically are the same citation, whatever key the
-- markdown used. \ref needs a second LaTeX pass to resolve; tectonic and
-- latexmk both re-run to convergence on their own.

if FORMAT ~= "latex" and FORMAT ~= "beamer" then
  return {}
end

local seen = {}   -- note text -> label number
local count = 0

local function label_inline(n)
  return pandoc.RawInline("latex", "\\label{fn:" .. n .. "}")
end

function Note(el)
  local key = pandoc.utils.stringify(el.content)
  if key == "" then
    return nil                       -- nothing to compare on; leave it alone
  end

  local prev = seen[key]
  if prev then
    -- \footnotemark would advance the counter; \ref does not, and prints the
    -- number the reader already saw.
    return pandoc.RawInline("latex", "\\textsuperscript{\\ref{fn:" .. prev .. "}}")
  end

  count = count + 1
  seen[key] = count

  local blocks = el.content
  local last = blocks[#blocks]
  if last and (last.t == "Para" or last.t == "Plain") then
    table.insert(last.content, label_inline(count))
  else
    table.insert(blocks, pandoc.Plain({label_inline(count)}))
  end
  return el
end
