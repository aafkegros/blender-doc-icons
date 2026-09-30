local icons
local instance = 0

local function escape_attribute(text)
  return (text:gsub("&", "&amp;"):gsub('"', "&quot;")
    :gsub("<", "&lt;"):gsub(">", "&gt;"))
end

return {
  ["blender"] = function(args, kwargs)
    if not args[1] then
      error("Expected an icon name: {{< blender scene_data >}}")
    end
    local name = pandoc.utils.stringify(args[1]):lower()
    if not name:match("^[a-z0-9_]+$") then
      error("Invalid Blender icon name: " .. name)
    end
    if not icons then
      local file = assert(io.open(quarto.utils.resolve_path("icons.json"), "r"))
      local contents = file:read("*a")
      file:close()
      icons = quarto.json.decode(contents)
    end
    local html = icons[name]
    if not html then
      error("Unknown Blender icon '" .. name .. "'. Use 'blender-icons list' to see available names.")
    end
    local label = kwargs.label and pandoc.utils.stringify(kwargs.label) or ""
    if not quarto.doc.is_format("html") then
      return pandoc.Str(label ~= "" and label or ("[" .. name:gsub("_", " ") .. "]"))
    end
    quarto.doc.add_html_dependency({
      name = "blender-icons", version = "0.1.0", stylesheets = {"icons.css"}
    })
    instance = instance + 1
    -- Templates already namespace IDs; make each use of a template unique too.
    html = html:gsub("bi%-%x+%-", function(prefix)
      return prefix .. "q" .. instance .. "-"
    end)
    if label ~= "" then
      html = html:gsub('aria%-hidden="true"', function()
        return 'role="img" aria-label="' .. escape_attribute(label) .. '"'
      end, 1)
    end
    return pandoc.RawInline("html", html)
  end
}
