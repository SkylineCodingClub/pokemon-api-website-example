pokequery = {};

pokequery.Pokedex = Backbone.Model.extend({
    initialize: function(options) {
        var self = this;
        self.url = "/data/api/v1/pokedex/1/";
        self.fetch().done(function() {
            self.trigger("ready");
        });
    },
});

pokequery.pokedexEntry = _.template([
    '<div class="pokedex-entry" data-resource="<%= resource_uri %>" ><%= name %></div>'
].join("\n"));

pokequery.pokedexList = _.template([
    '<div class="pokedex-list">',
    '</div>',
    '<div class="pokemon-data">',
    '</div>',
].join("\n"));

pokequery.pokedexData = _.template([
    '<div class="pokemon-head">',
        '<div class="pokemon-title"></div>',
        '<div class="pokemon-type"></div>',
    '</div>',
    '<div class="pokemon-picture"></div>',
].join("\n"));

$(function() {
    pokequery.pokedex_view = new pokequery.PokedexView({
        model: new pokequery.Pokedex(),
        el: $(".main_section"),
    });
});


pokequery.PokedexView = Backbone.View.extend({
    events: {
        "click .pokedex-entry": "displayData",
    },
    template: pokequery.pokedexList,
    initialize: function(options) {
        var self = this;
        self.model = options.model;
        self.dataView = new pokequery.PokemonDataView({
            el: self.$(".pokemon-data"),
        });
        self.listenTo(self.model, "ready", self.render);
        self.render();
    },
    render: function() {
        var self = this;
        self.$el.html(self.template());
        _.each(_.sortBy(self.model.get('pokemon'), ['name']), function(pokemon) {
            self.$(".pokedex-list").append(pokemon).append(
                pokequery.pokedexEntry(pokemon)
            );
        });
        self.dataView.setElement(self.$(".pokemon-data"));
    },
    displayData: function(e) {
        var self = this;
        var resource_url = $(e.currentTarget).attr('data-resource');
        $(".pokedex-entry").removeClass("selected");
        $(e.currentTarget).addClass("selected");
        var model = new pokequery.PokemonData({
            url: resource_url,
        });
        model.once('ready', function() {
            self.dataView.changeModel(model);
        });
    },
});

pokequery.PokemonData = Backbone.Model.extend({
    initialize: function(options) {
        var self = this;
        self.url = "/data/"+options.url;
        self.fetch().done(function() {
            self.trigger("ready");
        });
    },
});


pokequery.PokemonDataView = Backbone.View.extend({
    template: pokequery.pokedexData,
    render: function() {
        var self = this;
        self.$el.html(self.template());
        self.$(".pokemon-title").html(self.model.get('name'));
        x = self.model;
        http://cdn.bulbagarden.net/upload/6/6d/306Aggron.png
        var src = "//img.pokemondb.net/sprites/black-white/normal/"+
            self.model.get('name').toLowerCase()+".png";
        if(self.model.get("national_id") > 649) {
            src = "//img.pokemondb.net/sprites/x-y/normal/"+
                self.model.get('name').toLowerCase()+".png";
        }
        self.$(".pokemon-picture").append($("<img>", {
            src: src,
        }));
        _.each(self.model.get('types'), function(type) {
            self.$(".pokemon-type").append($("<div>", {
                class: type.name,
                
            }).html(type.name));
        });
    },
    changeModel: function(model) {
        var self = this;
        self.model = model;
        x = model;
        self.render();
    },
});
