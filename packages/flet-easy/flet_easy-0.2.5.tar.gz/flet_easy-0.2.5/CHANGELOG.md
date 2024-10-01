# Flet-Easy changelog

## v0.2.5 (30/09/24)

* Update links for the new repository

## 0.2.4 (03/09/24)

* ⚡The speed of the router is improved to more than twice as fast.
  
* Ways to install Flet-Easy. [[Doc](https://flet-easy.pages.dev/0.2.0/installation/)]
  
* Add `go_back` method. [[Doc](https://flet-easy.pages.dev/0.2.0/how-to-use/#methods/)]
  
* Ruff configuration update (>=0.4.4).
  
* Supporting the use of class to create a view. [[Doc](https://flet-easy.pages.dev/0.2.0/add-pages/through-classes/)]
  
* Bug fixes found in previous changes.
  
* Documentation improvements and updates. [[view](https://flet-easy.pages.dev/0.2.0/)]

### **Changes in the api:**

New method added in Datasy (data) [[Doc](https://flet-easy.pages.dev/0.2.0/how-to-use/#datasy-data/)]

* `history_routes` : Get the history of the routes.
* `go_back` : Method to go back to the previous route.

### **🔎Note**

* Now `page.go()` and `data.go()` work similarly to go to a page (View), the only difference is that `data.go()` checks for url redirects when using `data.redirect()`.

* Compatible with previous `versions 0.2.*`.

---

## 0.2.2 (04/05/24)

* Fix sensitivity in url with capital letters.
* Fix 'back' button in dashboard page app bar not working.
* Fix error caused by `Timeout waiting invokeMethod`.

---

## 0.2.1 (25/04/24)

* Fix page loading twice.

---

## 0.2.0 (17/04/24)

* Compatibility and optimization code for `flet>=0.21`.
* Fix async.
* Automatic routing ([Docs](https://flet-easy.pages.dev/0.2.0/add-pages/in-automatic/))
* Add the `title` parameter to the `page` decorator. ([Docs](https://flet-easy.pages.dev/0.2.0/how-to-use/#example_1))
* Add `JWT` support for authentication sessions in the data parameter ([Docs](https://flet-easy.pages.dev/0.2.0/basic-JWT/))
* Add a `Cli` to create a project structure based on the MVC design pattern. ([Docs](https://flet-easy.pages.dev/0.2.0/cli-to-create-app/))
* Middleware Support. ([Docs](https://flet-easy.pages.dev/0.2.0/middleware/))
* Add more simplified Ref control ([Docs](https://flet-easy.pages.dev/0.2.0/ref/))
* Enhanced Documentation.
* Ruff Integration.

### **Changes in the api:**

* The `async` methods have been removed, as they are not necessary.
* Change `update_login` method to `login` of Datasy. ([Docs](https://flet-easy.pages.dev/0.2.0/Customized-app/Route-protection/#login))
* Change `logaut` method to `logout` of Datasy. ([Docs](https://flet-easy.pages.dev/0.2.0/Customized-app/Route-protection/#logout))
* Changed function parameter decorated on `login` | `(page:ft.Page -> data:fs:Datasy)` ([Docs](https://flet-easy.pages.dev/0.2.0/Customized-app/Route-protection/))
* Changed function parameter decorated on `config_event_handler` | `(page:ft.Page -> data:fs:Datasy)` ([Docs](https://flet-easy.pages.dev/0.2.0/Customized-app/Events/))

---

## 0.1.3 (11/03/2024)

* Flet installation is required to use Flet-Easy.
* Fixed error when running the application with `flet v0.21.0`
* Fixed packing when compiling an apk.
* Compatibility with `flet<=0.22.0`

---

## 0.1.1 (31/01/2024)

* Parameter `proctect_route` changed to `protected_route` of `page` decorator ([Docs](https://flet-easy.pages.dev/0.1.0/customized-app/route-protection/))
* Added functionality to share data between pages in a more controlled way ([Docs](https://flet-easy.pages.dev/0.1.0/data-sharing-between-pages/))

---

## 0.1.0

* Easy to use (**hence the name**).
* Facilitates `flet` event handling.
* Simple page routing (There are three ways) for whichever one suits you best. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/dynamic-routes/))
* App construction with numerous pages and custom flet configurations for desktop, mobile and web sites.
* Provides a better construction of your code, which can be scalable and easy to read (it adapts to your preferences, there are no limitations).
* Dynamic routing, customization in the routes for greater accuracy in sending data. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/dynamic-routes/#custom-validation))
* Routing protection ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/customized-app/route-protection/))
* Custom Page 404 ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/customized-app/page-404/))
* Asynchronous support.
* Working with other applications. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/data-sharing-between-pages/))
* Easy integration of `on_keyboard_event` in each of the pages. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/events/keyboard-event/))
* Use the percentage of the page width and height of the page with `on_resize`. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/events/on-resize/))
* `ResponsiveControlsy` control to make the app responsive, useful for desktop applications. ([**`Docs`**](https://flet-easy.pages.dev/0.1.0/responsiveControlsy/))
* Soporta Application Packaging para su distribución. ([view](https://flet.dev/docs/publish))
