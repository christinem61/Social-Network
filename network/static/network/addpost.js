text_f = document.querySelector("#add-text");
btn = document.querySelector("#add-btn");
root = document.querySelector("#root");
btn.addEventListener("click", () => {
  text = text_f.value;

  if (text.length > 0) {
    form = new FormData();
    form.append("post", text.trim());
    fetch("/addpost/", {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.status == 201) {
          add_html(res.post_id, res.username, text.trim(), res.timestamp, `/u/${res.username}`);
          text_f.value = "";
        }
      });
  }
});

function make_div(className) {
  div = document.createElement("div");
  div.setAttribute("class", className);
  return div;
}

function add_html(id, username, post, time, link) {
  div1 = make_div("card");
  div1.setAttribute("style", "padding:23px");
  div2 = document.createElement("div");
  div2.setAttribute("style", "display:flex");
  a1 = document.createElement("a");
  a1.setAttribute("href", link);
  a1.setAttribute("style","font-size:18px")
  a1.textContent = username;
  div3 = make_div("w-100 d-flex justify-content-end");
  p1 = document.createElement("p");
  p1.setAttribute("style", "color:gray; padding-bottom:10px");
  p1.textContent = time+"            "
  span2 = document.createElement("span");
  span2.setAttribute("class", "text-primary edit");
  span2.setAttribute("style", "font-weight:600")
  span2.textContent = "Edit";
  span2.setAttribute("data-id", id);
  span2.setAttribute("id", `edit-btn-${id}`);
  span2.addEventListener("click", () => {
    edit_handeler(span2);
  });
  div4 = document.createElement("div");
  div4.setAttribute("style", "display:flex; justify-content:space-between")
  span3 = document.createElement("span");
  span3.setAttribute("id", `post-content-${id}`);
  span3.textContent = post;
  textarea = document.createElement("textarea");
  textarea.setAttribute("id", `post-edit-${id}`);
  textarea.setAttribute("data-id", id);
  textarea.setAttribute("style", "display:none;");
  textarea.setAttribute("cols", "130")
  textarea.textContent = post;
  textarea.addEventListener("keyup", (e) => {
    if (e.keyCode == 13 && e.shiftKey) return;
    if (e.keyCode === 13) edit_handeler(textarea);
  });
  div5 = make_div("like");
  img = document.createElement("img");
  img.setAttribute("class", "liked");
  img.setAttribute("data-id", id);
  img.setAttribute("id", `post-like-${id}`);
  img.setAttribute("data-is_liked", "no");
  img.setAttribute("width","45");
  img.setAttribute("height","25");
  img.setAttribute("src", "https://img.icons8.com/carbon-copy/100/000000/like--v2.png");
  like_handeler(img);
  span4 = document.createElement("span");
  span4.setAttribute("id", `post-count-${id}`);
  span4.textContent = "0";
  root.appendChild(div1);
  div1.appendChild(div2);
  div2.appendChild(a1);
  div2.appendChild(div3);
  div3.appendChild(p1);
  p1.appendChild(span2);
  div1.appendChild(div4);
  div4.appendChild(span3);
  div4.appendChild(textarea);
  div4.appendChild(div5);
  div5.appendChild(img);
  div5.appendChild(span4);
}