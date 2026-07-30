-- Drop the body H1 that repeats the YAML `title:` on one-pagers.
-- Both are wanted in the markdown (the H1 is what renders in the repo and in
-- the interactive viewer), but in the PDF \maketitle already prints it, and
-- the duplicate costs vertical space the page cannot spare.
local dropped = false

function Header(el)
  if el.level == 1 and not dropped then
    dropped = true
    return {}
  end
end
