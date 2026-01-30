-- ignore-spacing.lua (robust)
-- Removes LaTeX spacing commands that leak as text in HTML,
-- and drops orphan paragraphs that literally render as "1em".

local function zap_spacing(tex)
  tex = tex:gsub("\\onehalfspacing", "")
  tex = tex:gsub("\\doublespacing", "")
  tex = tex:gsub("\\singlespacing", "")
  tex = tex:gsub("\\setstretch%s*%b{}", "")
  tex = tex:gsub("\\vspace%*?%b{}", "")
  tex = tex:gsub("\\smallskip", "")
  tex = tex:gsub("\\medskip", "")
  tex = tex:gsub("\\bigskip", "")
  return tex
end

function RawBlock(el)
  if el.format == "latex" then
    local t = zap_spacing(el.text)
    if t == "" then return {} end
    el.text = t
  end
  return el
end

function RawInline(el)
  if el.format == "latex" then
    local t = zap_spacing(el.text)
    if t == "" then return {} end
    el.text = t
  end
  return el
end

-- Helper to stringify inline content
local function stringify(inlines)
  local acc = {}
  for i = 1, #inlines do
    if inlines[i].text then table.insert(acc, inlines[i].text) end
  end
  return table.concat(acc)
end

-- Drop paragraphs that are literally "1em" or just whitespace
function Para(el)
  local s = stringify(el.content):gsub("%s+", "")
  if s == "" or s == "1em" then
    return {}
  end
  return el
end
