# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashCarousel(Component):
    """A DashCarousel component.
DashCarousel is a component that creates an interactive carousel/slider
using Swiper.js. It supports various features like autoplay, navigation,
pagination, and custom effects.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- activeIndex (number; default 0):
    The index of the currently active slide.

- activeSlideAlt (string; default ''):
    The alt text of the currently active slide.

- autoplay (dict; default {    delay: 3000,    disableOnInteraction: False}):
    Configuration object for autoplay behavior.

    `autoplay` is a dict with keys:

    - delay (number; optional):
        Delay between transitions (in ms).

    - disableOnInteraction (boolean; optional):
        Whether to pause autoplay on user interaction.

- autoplayEnabled (boolean; default False):
    Whether autoplay is enabled.

- carouselEffect (dict; default {    opacityStep: 0.33,    scaleStep: 0.2,    sideSlides: 2}):
    Configuration object for the carousel effect.

    `carouselEffect` is a dict with keys:

    - opacityStep (number; optional):
        Step value for opacity change between slides.

    - scaleStep (number; optional):
        Step value for scale change between slides.

    - sideSlides (number; optional):
        Number of side slides visible.

- className (string; default ''):
    Additional CSS class for the root element.

- grabCursor (boolean; default True):
    Whether to change the cursor to \"grab\" while swiping.

- loop (boolean; default True):
    Whether to enable continuous loop mode.

- navigation (boolean; default True):
    Whether to display navigation buttons.

- pagination (boolean; default True):
    Whether to display pagination dots.

- slides (list of dicts; required):
    An array of objects representing the slides in the carousel. Each
    object should have src, alt, title, and description properties.

    `slides` is a list of dicts with keys:

    - alt (string; optional)

    - description (string; optional)

    - src (string; required)

    - title (string; optional)

- slidesPerView (number; default 3):
    Number of slides per view.

- swiperOptions (dict; optional):
    Additional options to pass directly to Swiper instance."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_swiper'
    _type = 'DashCarousel'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, slides=Component.REQUIRED, className=Component.UNDEFINED, carouselEffect=Component.UNDEFINED, navigation=Component.UNDEFINED, pagination=Component.UNDEFINED, autoplayEnabled=Component.UNDEFINED, autoplay=Component.UNDEFINED, loop=Component.UNDEFINED, grabCursor=Component.UNDEFINED, slidesPerView=Component.UNDEFINED, swiperOptions=Component.UNDEFINED, activeIndex=Component.UNDEFINED, activeSlideAlt=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'activeIndex', 'activeSlideAlt', 'autoplay', 'autoplayEnabled', 'carouselEffect', 'className', 'grabCursor', 'loop', 'navigation', 'pagination', 'slides', 'slidesPerView', 'swiperOptions']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'activeIndex', 'activeSlideAlt', 'autoplay', 'autoplayEnabled', 'carouselEffect', 'className', 'grabCursor', 'loop', 'navigation', 'pagination', 'slides', 'slidesPerView', 'swiperOptions']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['slides']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashCarousel, self).__init__(**args)
